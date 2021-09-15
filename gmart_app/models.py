from django.db import models
from django.conf import settings

#  Models:  https://docs.djangoproject.com/en/3.1/ref/models/fields/#model-field-types
#  List of Database Field Types:  https://docs.djangoproject.com/en/3.1/ref/models/fields/#model-field-types 


class Department (models.Model):
    Department_Name = models.CharField(max_length = 100, unique = True)

    def __str__(self):
        return self.Department_Name


class Product(models.Model):
    Product_Name = models.CharField(max_length = 100)
    Product_Department = models.ForeignKey(Department, on_delete = models.CASCADE)
    Product_Description = models.TextField()
    Product_Price = models.DecimalField(max_digits = 7, decimal_places = 2)
    Product_Quantity = models.IntegerField()
    Product_Highlights = models.TextField()
    Product_Details = models.TextField()
    Product_Image_Primary = models.ImageField(default='no_product.jpg', upload_to='product_images')

    def __str__(self):
        return f'{self.Product_Name} -- ${self.Product_Price}'


class Order(models.Model):
    Order_User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Order_Product = models.ManyToManyField(Product, through='OrderItem')
    Order_Created = models.DateTimeField(auto_now_add=True)
    Order_Date = models.DateTimeField()
    Order_Ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.Order_User.username


class OrderItem(models.Model):
    OrderItem_Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    OrderItem_Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    OrderItem_Quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.OrderItem_Product}'