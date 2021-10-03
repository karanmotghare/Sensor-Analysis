# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Location(models.Model):
    loc_id = models.AutoField(primary_key=True)
    loc_name = models.CharField(max_length=255)
    org = models.ForeignKey('Organisation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'location'


class Organisation(models.Model):
    org_id = models.AutoField(primary_key=True)
    org_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'organisation'


class Sensor(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    sensor_name = models.CharField(max_length=255)
    sg = models.ForeignKey('SensorGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sensor'


class SensorActualData(models.Model):
    record_id = models.AutoField(primary_key=True)
    sensor = models.ForeignKey(Sensor, models.DO_NOTHING)
    data_value = models.FloatField()
    record_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor_actual_data'


class SensorGenData(models.Model):
    record_id = models.AutoField(primary_key=True)
    sensor = models.ForeignKey(Sensor, models.DO_NOTHING)
    version_id = models.IntegerField()
    from_data = models.FloatField()
    to_data = models.FloatField()
    from_time = models.DateTimeField(blank=True, null=True)
    to_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor_gen_data'


class SensorGroup(models.Model):
    sg_id = models.AutoField(primary_key=True)
    sg_name = models.CharField(max_length=255)
    loc = models.ForeignKey(Location, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sensor_group'


class SuperAdmins(models.Model):
    username = models.CharField(primary_key=True, max_length=255)
    pwd = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'super_admins'


class Users(models.Model):
    username = models.CharField(primary_key=True, max_length=255)
    pwd = models.CharField(max_length=255)
    position = models.CharField(max_length=9)
    org = models.ForeignKey(Organisation, models.DO_NOTHING, blank=True, null=True)
    created_by = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users'
