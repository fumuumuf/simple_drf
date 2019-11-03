from django.db import models, transaction
from django.db.models import Max, Min, Q
from django.db.models.expressions import RawSQL, Subquery, Value, F
from django.db.models.functions import Coalesce

from accounts.models import User


class Tag(models.Model):
    name = models.CharField('タグ名', max_length=120)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Category(models.Model):
    name = models.CharField('name', max_length=120, default='no title')


class Article(models.Model):
    """
    記事
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='記事の作者')
    title = models.CharField('タイトル', max_length=120, default='no title')
    body = models.TextField('本文')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles', verbose_name='タグ', help_text='記事につけるタグ')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, default=None, )

    def __str__(self):
        return f'{self.id} - {self.title}'


class FFMQuerySet(models.QuerySet):
    # def get_parents(self):
    #     return self.filter(role='A')
    #
    # def get_parent(self):
    #     return self.filter(role='E')
    #
    pass


INT_MAX = 0x7fffffff


class FFMManager(models.Manager):
    """
    """

    def get_queryset(self):
        return FFMQuerySet(self.model, using=self._db)

    def sub_tree(self, base, limit_depth=None, with_top=False):
        """
        base の 子孫ノードを検索
        TODO: これら filter 系 は queryset に移動してもよいかも
        Args:
            base (FertileForestNode): ベースとなる FF インスタンス. このインスタンスの子孫ノードを取得
            limit_depth (int): 何世代まで取得するか？
            with_top: base ノードも含めるかどうか
        """
        tree_start_cond = Q(depth__gt=base.depth) & Q(queue__gt=base.queue)
        if with_top:
            tree_start_cond = tree_start_cond | Q(id=base.id)

        # HACK: RawSQL 使わずできるか？
        # x はダミー列. これにより annotate で取得でき, Subquery に渡せる.
        tree_end_cond_qs = self.annotate(x=RawSQL("'0'", [])).values('x'). \
            filter(queue__gt=base.queue, depth__lte=base.depth). \
            annotate(min_queue=Min('queue'))
        qs = self.filter(tree_start_cond,
                         queue__lt=Coalesce(Subquery(tree_end_cond_qs.values('min_queue')[:1]), Value(INT_MAX)))
        if limit_depth:
            qs = qs.filter(depth__lte=base.depth + limit_depth)
        return qs

    def find_tree(self, root_id, limit_depth=None):
        base = self.get(id=root_id)
        return self.sub_tree(base, limit_depth=limit_depth, with_top=True)

    def find_ancestor(self, node, limit_depth=None):
        """
        先祖ノードの検索
        Args:
            node (Union[int, FertileForestNode]): 対象ノードまたはその id
            limit_depth (int): 何世代前まで取得するか？
        Returns:
            queryset
        """
        if isinstance(node, int):
            node = self.get(id=node)

        sub_qs = FertileForestNode.objects.filter(queue__lt=node.queue, depth__lt=node.depth, )
        if limit_depth:
            sub_qs = sub_qs.filter(depth__gte=node.depth - limit_depth)
        sub_qs = sub_qs.values('depth').annotate(max_queue=Max('queue'))

        return self.filter(queue__in=Subquery(sub_qs.values('max_queue')))

    def create(self, **kwargs):
        """
        Create a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        if 'parent' in kwargs:
            parent = kwargs.pop('parent')
            return self.add_node(parent, **kwargs)
        elif 'depth' not in kwargs:
            return self.add_root(**kwargs)
        else:
            return super(FFMManager, self).create(**kwargs)

    def add_root(self, **params):
        """
        ルートの追加
        Args:
            **kwargs:
        Returns:
            FertileForestNode: 追加ノード
        """
        params['depth'] = 0
        mq = self.aggregate(mq=Max('queue'))['mq']
        if mq is None:
            params['queue'] = 0
        else:
            params['queue'] = mq + 1
        return self.create(**params)

    def add_node(self, base, **params):
        """
        ノードの追加
        Args:
            base (Union[int, FertileForestNode]): 親ノードのインスタンスまたはその id
            **params: ノードのパラメータ
        Returns:
            FertileForestNode: 追加ノード
        """
        if not base:
            return self.add_root(**params)

        if isinstance(base, int):
            base = self.get(id=base)

        with transaction.atomic():  # start transaction
            self.filter(queue__gt=base.queue).update(queue=F('queue') + 1)
            params.update({
                'queue': base.queue + 1,
                'depth': base.depth + 1,
            })
            return self.create(**params)

    def delete_descendants(self, base, with_top=False):
        """
        base の子孫ノードを削除します.
        base ノードも削除する場合は with_top に True を指定してください.
        Args:
            base (Union[int, FertileForestNode]): ノードのインスタンスまたはその id
            with_top: base も一緒に削除するかどうか
        Returns: delete の結果
        """
        if isinstance(base, int):
            base = self.get(id=base)
        return self.sub_tree(base, with_top=with_top).delete()

    def delete_only_node(self, node):
        """
        Args:
            node (FertileForestNode): このノードのみを削除し, 子孫ノードは残します.
        """
        with transaction.atomic():  # start transaction
            node.delete()
            update_nodes = self.sub_tree(node)
            update_nodes.update(depth=F('depth') - Value(1))
        return True


class FertileForestNode(models.Model):
    objects = FFMManager()
    depth = models.PositiveIntegerField(editable=False)
    queue = models.PositiveIntegerField(editable=False)

    def __str__(self):
        return f'({self.depth}, {self.queue})'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(FertileForestNode, self).save()

    class Meta:
        abstract = True


class Comment(FertileForestNode):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=128, default='comment')
