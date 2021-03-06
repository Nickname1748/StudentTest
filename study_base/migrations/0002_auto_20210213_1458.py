# Generated by Django 3.1.4 on 2021-02-13 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('study_base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlannedTest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('begin_date', models.DateTimeField(verbose_name='Begin date')),
                ('end_date', models.DateTimeField(verbose_name='End date')),
                ('student_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='study_base.studentgroup', verbose_name='Student group')),
            ],
        ),
        migrations.CreateModel(
            name='TestAttempt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True, verbose_name='Start date')),
                ('finish_date', models.DateTimeField(null=True, verbose_name='Finish date')),
                ('result', models.FloatField(null=True, verbose_name='Result')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
        ),
        migrations.CreateModel(
            name='TestModule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='TestTask',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_description', models.TextField(verbose_name='Task description')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_base.testmodule', verbose_name='Module')),
            ],
        ),
        migrations.CreateModel(
            name='TestTaskChoiceItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Text')),
                ('is_right', models.BooleanField(verbose_name='Right')),
            ],
        ),
        migrations.CreateModel(
            name='TestTaskMultipleChoice',
            fields=[
                ('testtask_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='study_base.testtask')),
            ],
            bases=('study_base.testtask',),
        ),
        migrations.CreateModel(
            name='TestTaskSingleChoice',
            fields=[
                ('testtask_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='study_base.testtask')),
            ],
            bases=('study_base.testtask',),
        ),
        migrations.CreateModel(
            name='TestTaskText',
            fields=[
                ('testtask_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='study_base.testtask')),
                ('answer', models.CharField(max_length=255, verbose_name='Answer')),
            ],
            bases=('study_base.testtask',),
        ),
        migrations.CreateModel(
            name='TestAttemptTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=255, null=True, verbose_name='Answer')),
                ('attempt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_base.testattempt', verbose_name='Test attempt')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_base.testtask', verbose_name='Task')),
            ],
        ),
        migrations.AddField(
            model_name='testattempt',
            name='tasks',
            field=models.ManyToManyField(through='study_base.TestAttemptTask', to='study_base.TestTask', verbose_name='Tasks'),
        ),
        migrations.AddField(
            model_name='testattempt',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='study_base.plannedtest', verbose_name='Test'),
        ),
        migrations.CreateModel(
            name='TestTaskSingleChoiceItem',
            fields=[
                ('testtaskchoiceitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='study_base.testtaskchoiceitem')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_base.testtasksinglechoice', verbose_name='Task')),
            ],
            bases=('study_base.testtaskchoiceitem',),
        ),
        migrations.CreateModel(
            name='TestTaskMultipleChoiceItem',
            fields=[
                ('testtaskchoiceitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='study_base.testtaskchoiceitem')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_base.testtaskmultiplechoice', verbose_name='Task')),
            ],
            bases=('study_base.testtaskchoiceitem',),
        ),
        migrations.CreateModel(
            name='PlannedTestModular',
            fields=[
                ('plannedtest_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='study_base.plannedtest')),
                ('task_count', models.PositiveSmallIntegerField(verbose_name='Task count')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='study_base.testmodule', verbose_name='Module')),
            ],
            bases=('study_base.plannedtest',),
        ),
        migrations.CreateModel(
            name='PlannedTestManual',
            fields=[
                ('plannedtest_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='study_base.plannedtest')),
                ('tasks', models.ManyToManyField(to='study_base.TestTask', verbose_name='Tasks')),
            ],
            bases=('study_base.plannedtest',),
        ),
    ]
