from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator
from .models import *
from .forms import *



Page = 4
Col = 1

# 主页
def market(request):
    catgories = Catgory.objects.all
    page = 1
    goods = Good.objects.all()
    pages = Paginator(goods, Page)
    cols = Paginator(pages.page(page), Col)
    pagerange = pages.page_range
    goods = {}
    for i in cols.page_range:
        goods[f'good{i}'] = cols.page(i)
    content = {
        'catgories' : catgories,
        'homestatus' : 'active',

        'goods' : goods,
        'pagerange' : pagerange,
        'page' : page,
        'pagemethod' : 'marketpage',
    }
    return render(request, "market/market.html", content)

# 主页，换页
def marketpage(request, page):
    catgories = Catgory.objects.all
    goods = Good.objects.all()
    pages = Paginator(goods, Page)
    cols = Paginator(pages.page(page), Col)
    pagerange = pages.page_range
    goods = {}
    for i in cols.page_range:
        goods[f'good{i}'] = cols.page(i)
    content = {
        'catgories' : catgories,
        'homestatus' : 'active',

        'goods' : goods,
        'pagerange' : pagerange,
        'page' : int(page),
        'pagemethod' : 'marketpage',
    }
    return render(request, "market/market.html", content)

# 详情
def detail(request, pk):
    catgories = Catgory.objects.all
    good = Good.objects.get(id=pk)
    content = {
        'catgories' : catgories,
        'good' : good,
    }
    return render(request, "market/detail.html", content)

# 搜索结果展示
def search(request):
    catgories = Catgory.objects.all
    question = request.GET.get('keyword')
    goods = Good.objects.filter(名称__icontains=question)
    page = 1
    pages = Paginator(goods, Page)
    cols = Paginator(pages.page(page), Col)
    pagerange = pages.page_range
    goods = {}
    for i in cols.page_range:
        goods[f'good{i}'] = cols.page(i)
    content = {
        'catgories' : catgories,

        'goods' : goods,
        'pagerange' : pagerange,
        'page' : int(page),
        'question' : question,
        'pagemethod' : 'searchmovepage',
    }
    return render(request, "market/search.html", content)

# 搜索结果展示，分页
def searchpage(request, question, page):
    catgories = Catgory.objects.all
    question = question
    goods = Good.objects.filter(名称__icontains=question)
    pages = Paginator(goods, Page)
    pagerange = pages.page_range
    cols = Paginator(pages.page(page), Col)
    goods = {}
    for i in cols.page_range:
        goods[f'good{i}'] = cols.page(i)
    content = {
        'catgories' : catgories,
        'goods' : goods,

        'pagerange' : pagerange,
        'page' : int(page),
        'question' : question,
        'pagemethod' : 'searchmovepage',
    }
    return render(request, 'market/search.html', content)

# 搜索换页
def searchmovepage(request, question, page):
    action = request.GET.get('action')
    goods = Good.objects.filter(名称__icontains=question)
    pages = Paginator(goods, Page) # 每页Page个商品，决定分为几页
    pagerange = pages.page_range
    currentpage = pages.page(page)
    if currentpage.has_other_pages:
        if action == 'nex':
            if currentpage.has_next and ((int(page)+1) in pagerange):
                return redirect(reverse('searchpage', kwargs={'page':int(page)+1, 'question' : question}))
            else:
                return redirect(reverse('searchpage', kwargs={'page':int(page), 'question' : question}))
        elif action == 'pre':
            if currentpage.has_previous and ((int(page)-1) in pagerange):
                return redirect(reverse('searchpage', kwargs={'page':int(page)-1, 'question' : question}))
            else:
                return redirect(reverse('searchpage', kwargs={'page':int(page), 'question' : question}))
    else:
        return redirect(reverse('searchpage', kwargs={'page':int(page), 'question' : question}))

# # 用户设置
@login_required
def setting(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid(): #所有验证都通过
        # do something处理业务
            form.save()
            return HttpResponseRedirect('/market/setting')
        else:
            print(form.errors)
    content = {
        'form' : form,
    }
    return render(request, "market/setting.html", content)

# 发布
@login_required
def publish(request):
    catgories = Catgory.objects.all
    customer = request.user.customer
    form = GoodForm(initial={'发布者':customer})
    if request.method == "POST":
        form = GoodForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            data = form.cleaned_data
            catgory = Catgory.objects.get(分类=data['分类'][0])
            good = catgory.good_set.create(发布人=customer, 图片=data['图片'], 名称=data['名称'], 简介=data['简介'], 价格=data['价格'])
            for i in data['分类'][1:]:
                good.分类.add(i)
            good.save()
            return redirect(reverse('mypublish'))
        else:
            print(form.errors)
    content = {
        'catgories' : catgories,
        'publish_status' : 'active',

        'form' : form,
    }
    return render(request, "market/publish.html", content)

# 注册用户的发布，主页
def userpublish(request, pk):
    catgories = Catgory.objects.all
    page = 1
    customer = Customer.objects.get(id=pk)
    customerid = customer.id
    goods = Good.objects.filter(发布人=customer)
    pages = Paginator(goods, Page)
    cols = Paginator(pages.page(page), Col)
    pagerange = pages.page_range
    goods = {}
    for i in cols.page_range:
        goods[f'good{i}'] = cols.page(i)
    content = {
        'catgories' : catgories,
        'mypublish_status' : 'active', # 控制导航栏“我的发布”激活状态

        'goods' : goods,
        'customerid' : customerid,
        'page' : page,
        'pagerange' : pagerange,
        'pagemethod' : 'userpublishpage',
    }
    return render(request, "market/userpublish.html", content)

# 注册用户的发布
def userpublishpage(request, pk, page):
    catgories = Catgory.objects.all
    customer = Customer.objects.get(id=pk)
    goods = Good.objects.filter(发布人=customer)
    pages = Paginator(goods, Page)
    cols = Paginator(pages.page(page), Col)
    pagerange = pages.page_range
    goods = {}
    for i in cols.page_range:
        goods[f'good{i}'] = cols.page(i)
    content = {
        'catgories' : catgories,
        'mypublish_status' : 'active', # 控制导航栏“我的发布”激活状态

        'goods' : goods,
        'customerid' : pk,
        'page' : int(page),
        'pagerange' : pagerange,
    }
    return render(request, "market/userpublish.html", content)

# 注册用户的发布，分页
def userpublishmovepage(request, pk, page):
    action = request.GET.get('action')
    customer = Customer.objects.get(id=pk)
    goods = Good.objects.filter(发布人=customer)
    pages = Paginator(goods, Page) # 每页Page个商品，决定分为几页
    pagerange = pages.page_range # 分页栏的数字
    currentpage = pages.page(page)
    if currentpage.has_other_pages:
        if action == 'nex':
            if currentpage.has_next and ((int(page)+1) in pagerange):
                return redirect(reverse('userpublishpage', kwargs={'page':int(page)+1, 'pk':pk}))
            else:
                return redirect(reverse('userpublishpage', kwargs={'page':page, 'pk':pk}))
        elif action == 'pre':
            if currentpage.has_previous and ((int(page)-1) in pagerange):
                return redirect(reverse('userpublishpage', kwargs={'page':int(page)-1, 'pk':pk}))
            else:
                return redirect(reverse('userpublishpage', kwargs={'page':page, 'pk':pk}))
    else:
        return redirect(reverse('userpublishpage', kwargs={'page':page, 'pk':pk}))

# 我的发布，主页
@login_required
def mypublish(request):
    catgories = Catgory.objects.all
    page = 1
    customer = request.user.customer
    goods = Good.objects.filter(发布人=customer)
    pages = Paginator(goods, Page)
    cols = Paginator(pages.page(page), Col)
    pagerange = pages.page_range
    goods = {}
    for i in cols.page_range:
        goods[f'good{i}'] = cols.page(i)
    content = {
        'catgories' : catgories,
        'mypublish_status' : 'active', # 控制导航栏“我的发布”激活状态

        'goods' : goods,
        'page' : page,
        'pagerange' : pagerange,
        'pagemethod' : 'mypublishpage',
    }
    return render(request, "market/mypublish.html", content)

# 我的发布
@login_required
def mypublishpage(request, page):
    catgories = Catgory.objects.all
    customer = request.user.customer
    goods = Good.objects.filter(发布人=customer)
    pages = Paginator(goods, Page)
    cols = Paginator(pages.page(page), Col)
    pagerange = pages.page_range
    goods = {}
    for i in cols.page_range:
        goods[f'good{i}'] = cols.page(i)
    content = {
        'catgories' : catgories,
        'mypublish_status' : 'active', # 控制导航栏“我的发布”激活状态

        'goods' : goods,
        'page' : int(page),
        'pagerange' : pagerange,
        'pagemethod' : 'mypublishpage',
    }
    return render(request, "market/mypublish.html", content)

# 更改商品页面
@login_required
def modify(request, pk):
    catgories = Catgory.objects.all
    customer = request.user.customer
    good =  Good.objects.get(id=pk)
    form = GoodForm(instance=good, initial={'发布者':customer})
    if request.method == "POST":
        form = GoodForm(request.POST, request.FILES, instance=good)
        if form.is_valid():
            form.save()
            return redirect(reverse('mypublish'))
        else:
            print(form.errors)
    content = {
        'catgories' : catgories,
        'form' : form
    }
    return render(request, "market/modify.html", content)


# 删除发布商品
@login_required
def delpublish(request, pk):
    Good.objects.filter(id=pk).delete()
    return redirect(reverse('mypublish'))

# 收藏商品
@login_required
def collect(request, pk):
    catgories = Catgory.objects.all
    customer = request.user.customer
    good = Good.objects.get(id=pk)
    Collect(收藏人=customer, 商品=good).save()
    return redirect(reverse('mycollect'))

# 查看收藏的商品
@login_required
def mycollect(request):
    catgories = Catgory.objects.all
    page = 1
    customer = request.user.customer
    collect = customer.collect_set.all()
    goods = [i.商品 for i in collect]
    pages = Paginator(goods, Page)
    cols = Paginator(pages.page(page), Col)
    pagerange = pages.page_range
    goods = {}
    for i in cols.page_range:
        goods[f'good{i}'] = cols.page(i)
    content = {
        'catgories' : catgories,
        'mycollectstatus' : 'active',

        'goods' : goods,
        'pagerange' : pagerange,
        'page' : page,
        'pagemethod' : 'mycollectpage',
    }
    return render(request, "market/mycollect.html", content)

# 查看收藏的商品，分页
@login_required
def mycollectpage(request, page):
    catgories = Catgory.objects.all
    customer = request.user.customer
    collect = customer.collect_set.all()
    goods = [i.商品 for i in collect]
    pages = Paginator(goods, Page)
    cols = Paginator(pages.page(page), Col)
    pagerange = pages.page_range
    goods = {}
    for i in cols.page_range:
        goods[f'good{i}'] = cols.page(i)
    content = {
        'catgories' : catgories,
        'mycollectstatus' : 'active',

        'goods' : goods,
        'pagerange' : pagerange,
        'page' : int(page),
        'pagemethod' : 'mycollectpage',
    }
    return render(request, "market/mycollect.html", content)

# 删除收藏的商品
@login_required
def delcollect(request, pk):
    customer = request.user.customer
    good = Good.objects.get(id=pk)
    Collect.objects.filter(收藏人=customer, 商品=good).delete()
    return redirect(reverse('mycollect'))

# 分类主页面
def catgory(request, pk):
    catgories = Catgory.objects.all
    page = 1
    catgory = Catgory.objects.get(id=pk)
    goods = Good.objects.filter(分类=catgory)
    pages = Paginator(goods, Page)
    cols = Paginator(pages.page(page), Col)
    pagerange = pages.page_range
    goods = {}
    for i in cols.page_range:
        goods[f'good{i}'] = cols.page(i)
    content = {
        'catgories' : catgories,
        'catgoryid' : catgory.id,
        'catgorystatus' : 'active',

        'goods' : goods,
        'pagerange' : pagerange,
        'page' : page,
        'pagemethod' : 'catgorypage',
    }
    return render(request, "market/catgory.html", content)
# 分类页面
def catgorypage(request, pk, page):
    catgories = Catgory.objects.all
    catgory = Catgory.objects.get(id=pk)
    goods = Good.objects.filter(分类=catgory)
    pages = Paginator(goods, Page)
    cols = Paginator(pages.page(page), Col)
    pagerange = pages.page_range
    goods = {}
    for i in cols.page_range:
        goods[f'good{i}'] = cols.page(i)
    content = {
        'catgories' : catgories,
        'catgoryid' : catgory.id,
        'catgorystatus' : 'active',

        'goods' : goods,
        'pagerange' : pagerange,
        'page' : int(page),
        'pagemethod' : 'catgorypage',
    }
    return render(request, "market/catgory.html", content)

# 分类页面换页
def catgorymovepage(request, pk, page):
    action = request.GET.get('action')
    method = request.GET.get('method')
    catgory = Catgory.objects.get(id=pk)
    catgoryid = catgory.id
    goods = Good.objects.filter(分类=catgory)
    pages = Paginator(goods, Page) # 每页Page个商品，决定分为几页
    pagerange = pages.page_range # 分页栏的数字
    currentpage = pages.page(page)
    if currentpage.has_other_pages:
        if action == 'nex':
            if currentpage.has_next and ((int(page)+1) in pagerange):
                return redirect(reverse(method, kwargs={'page':int(page)+1, 'pk':catgoryid}))
            else:
                return redirect(reverse(method, kwargs={'page':page, 'pk':catgoryid}))
        elif action == 'pre':
            if currentpage.has_previous and ((int(page)-1) in pagerange):
                return redirect(reverse(method, kwargs={'page':int(page)-1, 'pk':catgoryid}))
            else:
                return redirect(reverse(method, kwargs={'page':page, 'pk':catgoryid}))
    else:
        return redirect(reverse(method, kwargs={'page':page, 'pk':catgoryid}))

# 换页
def movepage(request, page):
    action = request.GET.get('action')
    method = request.GET.get('method')
    catgoryid = request.GET.get('catgoryid')
    goods = Good.objects.all()
    if method == 'marketpage':
        goods = Good.objects.all()
    elif method == 'mypublishpage':
        customer = request.user.customer
        goods = Good.objects.filter(发布人=customer)
    elif method == 'mycollectpage':
        customer = request.user.customer
        collect = customer.collect_set.all()
        goods = [i.商品 for i in collect]
    pages = Paginator(goods, Page) # 每页Page个商品，决定分为几页
    pagerange = pages.page_range # 分页栏的数字
    currentpage = pages.page(page)
    if currentpage.has_other_pages:
        if action == 'nex':
            if currentpage.has_next and ((int(page)+1) in pagerange):
                return redirect(reverse(method, kwargs={'page':int(page)+1}))
            else:
                return redirect(reverse(method, kwargs={'page':page}))
        elif action == 'pre':
            if currentpage.has_previous and ((int(page)-1) in pagerange):
                return redirect(reverse(method, kwargs={'page':int(page)-1}))
            else:
                return redirect(reverse(method, kwargs={'page':page}))
    else:
        return redirect(reverse(method, kwargs={'page':page}))