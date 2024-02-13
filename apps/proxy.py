from django.db.models import Manager

from apps.models import User


class UserManager(Manager):
    def get_queryset(self):
        return super(UserManager, self).get_queryset().filter(type_choice=User.Type.USERS)


class AdminManager(Manager):
    def get_queryset(self):
        return super(AdminManager, self).get_queryset().filter(type_choice=User.Type.ADMIN)


class CouriersManager(Manager):
    def get_queryset(self):
        return super(CouriersManager, self).get_queryset().filter(type_choice=User.Type.COURIER)


class ManagerProxy(Manager):
    def get_queryset(self):
        return super(ManagerProxy, self).get_queryset().filter(type_choice=User.Type.MANAGER)


class OperatorManager(Manager):
    def get_queryset(self):
        return super(OperatorManager, self).get_queryset().filter(type_choice=User.Type.OPERATOR)


class UserProxy(User):
    objects = UserManager()

    class Meta:
        proxy = True
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class CouriersProxy(User):
    objects = CouriersManager()

    class Meta:
        proxy = True
        verbose_name = 'Kuryer'
        verbose_name_plural = 'Kuryerlar'


class AdminProxy(User):
    objects = AdminManager()

    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Adminlar'


class MangerProxyModel(User):
    objects = ManagerProxy()

    class Meta:
        proxy = True
        verbose_name = 'Menejer'
        verbose_name_plural = 'Menejerlar'


class OperatorProxy(User):
    objects = AdminManager()

    class Meta:
        proxy = True
        verbose_name = 'Operator'
        verbose_name_plural = 'Operatorlar'

