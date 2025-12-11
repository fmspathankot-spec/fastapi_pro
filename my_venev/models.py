from tortoise import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
from typing import Optional


class User(Model):
    id = fields.IntField(pk=True,index=True)
    username = fields.CharField(max_length=255, unique=True,null=False)
    email = fields.CharField(max_length=255, unique=True,null=False)
    password = fields.CharField(max_length=255,null=False)
    is_active = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

class Bussness(Model):
        id = fields.IntField(pk=True,index=True)
        name = fields.CharField(max_length=255, unique=True,null=False)
        city = fields.CharField(max_length=255,null=False,default="unspecified")
        region = fields.CharField(max_length=255,null=False,default="unspecified")
        description = fields.TextField(null=True)
        logo = fields.CharField(max_length=255,null=True,default="default_logo.png")
        created_at = fields.DatetimeField(auto_now_add=True)
        updated_at = fields.DatetimeField(auto_now=True)
        user = fields.ForeignKeyField('models.User', related_name='bussness')

class Product(Model):
            id = fields.IntField(pk=True,index=True)
            name = fields.CharField(max_length=255, unique=True,null=False,index=True)
            category = fields.CharField(max_length=255,null=False,index=True)
            original_price = fields.DecimalField(max_digits=10, decimal_places=2)
            discount_price = fields.DecimalField(max_digits=10, decimal_places=2)
            percentage_discount = fields.IntField()
            Offer_expiration_date = fields.DatetimeField(null=False) 
            created_at = fields.DatetimeField(auto_now_add=True)
            updated_at = fields.DatetimeField(auto_now=True)
            bussness = fields.ForeignKeyField('models.Bussness', related_name='products')
            image = fields.CharField(max_length=255,null=True,default="default_image.png")

#user_pydantic = pydantic_model_creator(User, name="User",exclude=("is_active","created_at","updated_at"))
#user_pydantic_In = pydantic_model_creator(User, name="UserIn",exclude_readonly=True,exclude=("is_active","created_at","updated_at"))
#user_pydantic_Out = pydantic_model_creator(User, name="UserOut",exclude=("password"))
# In models.py
user_pydantic = pydantic_model_creator(User, name="User", exclude=("is_active","created_at","updated_at"))
user_pydantic_In = pydantic_model_creator(User, name="UserIn", exclude_readonly=True, exclude=("is_active","created_at","updated_at"))
user_pydantic_Out = pydantic_model_creator(User, name="UserOut", exclude=("password"))

bussness_pydantic = pydantic_model_creator(Bussness, name="Bussness")
bussness_pydantic_In = pydantic_model_creator(Bussness, name="BussnessIn",exclude_readonly=True)
#bussness_pydantic_Out = pydantic_model_creator(Bussness, name="BussnessOut",exclude=("user"))

product_pydantic = pydantic_model_creator(Product, name="Product")
product_pydantic_In = pydantic_model_creator(Product, name="ProductIn",exclude=("id","percentage_discount"))
#product_pydantic_Out = pydantic_model_creator(Product, name="ProductOut",exclude=("bussness"))


