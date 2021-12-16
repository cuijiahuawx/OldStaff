from django.urls import path
from . import views

urlpatterns = [
    path('', views.market, name='market'), # 主页
    # path('<str:page>', views.marketpage, name='marketpage'), # 主页, 换页


    # path('detail/<str:pk>/', views.detail, name='detail'), # 详情

    path('search/', views.search, name='search'), # 搜索
    path('search/<str:question>/<str:page>/', views.searchpage, name='searchpage'), # 搜索，分页
    path('searchmovepage/<str:question>/<str:page>', views.searchmovepage, name='searchmovepage'), # 换页

    path('setting/', views.setting, name='setting'), # 用户设置页面

    path('userpublish/<str:pk>/', views.userpublish, name='userpublish'), # 游客查看用户已发布商品
    path('userpublish/<str:pk>/<str:page>/', views.userpublishpage, name='userpublishpage'), # 游客查看用户已发布商品
    path('userpublishmovepage/<str:pk>/<str:page>/', views.userpublishmovepage, name='userpublishmovepage'), # 游客查看用户已发布商品, 换页

    path('publish/', views.publish, name='publish'), # 用户发布商品
    path('mypublish/', views.mypublish, name='mypublish'), # 用户已发布商品
    path('mypublish/<str:page>/', views.mypublishpage, name='mypublishpage'), # 用户已发布商品, 换页
    path('delpublish/<str:pk>/', views.delpublish, name='delpublish'), # 登录用户删除已发布商品
    path('modify/<str:pk>/', views.modify, name='modify'), # 更改商品信息

    path('collect/<str:pk>/', views.collect, name='collect'), # 收藏商品
    path('mycollect/', views.mycollect, name='mycollect'), # 查看收藏商品
    path('mycollect/<str:page>/', views.mycollectpage, name='mycollectpage'), # 查看收藏商品, 换页
    path('delcollect/<str:pk>/', views.delcollect, name='delcollect'), # 删除收藏商品

    path('catgory/<str:pk>/', views.catgory, name='catgory'), # 收藏商品
    path('catgory/<str:pk>/<str:page>/', views.catgorypage, name='catgorypage'), # 收藏商品
    path('catgorymovepage/<str:pk>/<str:page>/', views.catgorymovepage, name='catgorymovepage'), # 换页

    path('movepage/<str:page>/', views.movepage, name='movepage'), # 换页
    path('<str:page>/', views.marketpage, name='marketpage'), # 主页, 换页
]