from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Pipeline(models.Model):
    name = models.CharField(max_length=200)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Function(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    function = models.CharField(max_length=200)

    children = models.ManyToManyField("Function", related_name='+')

    def __str__(self):
        return str(self.name)


# class Rule(models.Model):
#     parent_id = models.ForeignKey(Function, related_name='%(class)s_parent', on_delete=models.CASCADE)
#     child_id = models.ForeignKey(Function, related_name='%(class)s_child', on_delete=models.CASCADE)


class Pipe(models.Model):
    pipeline_id = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    function_id = models.ForeignKey(Function, on_delete=models.DO_NOTHING)
