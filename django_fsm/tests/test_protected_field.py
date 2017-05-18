from django.db import models
from django.test import TestCase

from django_fsm import FSMField, transition


class ProtectedAccessModel(models.Model):
    status = FSMField(default='new', protected=True)

    @transition(field=status, source='new', target='published')
    def publish(self):
        pass

    class Meta:
        app_label = 'django_fsm'


class TestDirectAccessModels(TestCase):
    def test_no_direct_access(self):
        instance = ProtectedAccessModel()
        self.assertEqual(instance.status, 'new')

        def try_change():
            instance.status = 'change'

        self.assertRaises(AttributeError, try_change)

        instance.publish()
        instance.save()
        self.assertEqual(instance.status, 'published')

    def test_refresh_from_db(self):
        instance = ProtectedAccessModel()
        self.assertEqual(instance.status, 'new')

        instance.save()
        instance.refresh_from_db()
        self.assertEqual(instance.status, 'new')
