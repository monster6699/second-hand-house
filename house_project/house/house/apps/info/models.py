from django.db import models

# Create your models here.
# from users.models import  Follow


class BaseAttr(models.Model):
    houseType = models.CharField(max_length=100)
    floor = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    structure = models.CharField(max_length=50)
    inArea = models.CharField(max_length=50)
    buildType = models.CharField(max_length=50)
    buildHead = models.CharField(max_length=20)
    buildStruct = models.CharField(max_length=20)
    decorate = models.CharField(max_length=20)
    ladderHouPro = models.CharField(max_length=20)
    heatMethod = models.CharField(max_length=10)
    lift = models.CharField(max_length=10)
    period = models.CharField(max_length=10)
    address_wu = models.CharField(max_length=200)
    address_qu = models.CharField(max_length=200)
    address_detail = models.CharField(max_length=200)


    class Meta:
        db_table = 'tb_baseattr'
        verbose_name = '房屋基本属性信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.houseType


class TradeAttr(models.Model):
    listedTime = models.CharField(max_length=50)
    tradeOwershid = models.CharField(max_length=50)
    lastTransationTime = models.CharField(max_length=50)
    house_use = models.CharField(max_length=50)
    house_year = models.CharField(max_length=20)
    belongTo = models.CharField(max_length=20)
    mortgageInfo = models.CharField(max_length=200)
    roomBak = models.CharField(max_length=100)

    class Meta:
        db_table = 'tb_tradeattr'
        verbose_name = '房屋基本属性信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tradeOwershid




class Tag(models.Model):
    name=models.CharField(max_length=50)
    # housecharact = models.ForeignKey(HouseCharact,related_name='housecharact',on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_tag'
        verbose_name = '房屋标签'
        verbose_name_plural = verbose_name
# data_dict['selectData']=[address_wu,address_qu,address_detail,price,house_type,area,tag_list,build_head,floor,buildYear,decorate,house_use,lift,heat_method,trade_ownership,build_type]

class SelecttData(models.Model):
    address_wu = models.CharField(max_length=200)
    address_qu = models.CharField(max_length=200)
    address_detail = models.CharField(max_length=200)
    vides = models.CharField(max_length=200)
    price = models.IntegerField()
    houseType = models.CharField(max_length=200,null=True)
    area = models.CharField(max_length=200)
    tagList=models.CharField(max_length=200)
    houseHead = models.CharField(max_length=200,null=True)
    floor = models.CharField(max_length=200,null=True)
    buildYear = models.CharField(max_length=200,null=True)
    decorate = models.CharField(max_length=200,null=True)
    houseUse = models.CharField(max_length=200,null=True)
    lift = models.CharField(max_length=200,null=True)
    heatMethod = models.CharField(max_length=200,null=True)
    tradeOwnership = models.CharField(max_length=200,null=True)
    buildType = models.CharField(max_length=200,null=True)
    class Meta:
        db_table = 'tb_selectData'
        verbose_name = '房屋筛选表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tradeOwershid



class Container(models.Model):
    content =  models.CharField(max_length=600)

    class Meta:
        db_table = 'tb_container'
        verbose_name = '房屋筛选总表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tradeOwershid

class House(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    unitPrice = models.IntegerField()
    url = models.CharField(max_length=100)
    vide = models.CharField(max_length=100)
    focus = models.IntegerField()
    source = models.CharField(max_length=20)
    area = models.IntegerField()
    time = models.CharField(max_length=100)
    baseAttr = models.ForeignKey(BaseAttr,on_delete=models.CASCADE,related_name="house")
    tradeAttr = models.ForeignKey(TradeAttr,on_delete=models.CASCADE,related_name="house")
    selectData=models.ForeignKey(SelecttData,on_delete=models.CASCADE,related_name='house')
    Container=models.ForeignKey(Container,on_delete=models.CASCADE,related_name='house')
    # user=models.ForeignKey(User,related_name='house',default=None,null=True)
    # Tag = models.ForeignKey(Tag,on_delete=models.CASCADE,related_name="house")


    class Meta:
        db_table = 'tb_house'
        verbose_name = '房屋信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class Image(models.Model):
    name=models.CharField(max_length=200,default="暂无数据")
    url=models.CharField(max_length=200,default='https://s1.ljcdn.com/pegasus/redskull/images/common/blank.gif?_v=201904181525136')
    house = models.ForeignKey(House,related_name='image',on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_image'
        verbose_name = '房屋图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class HouseCharact(models.Model):
    name = models.CharField(max_length=50)
    content = models.CharField(max_length=600)
    Tag = models.ForeignKey(Tag,on_delete=models.CASCADE, related_name='housecharact')
    house = models.ForeignKey(House,on_delete=models.CASCADE, related_name='housecharact')

    class Meta:
        db_table = 'tb_housecharact'
        verbose_name = '房屋特色'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


