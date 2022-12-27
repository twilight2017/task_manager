from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import User

# django filter和django_tables2提供的Mixins
from django_tables2 import SingleTableView, RequestConfig
from django_filters.views import FilterView

# 定义过滤条件
from .filters import UserFilter

from .tables import UserTable

from .forms import UserForm
# Create your views here.


# 管理用户主界面
class UserAdminTableView(LoginRequiredMixin, SingleTableView, FilterView):
    filter = None
    # 使用UserFilter过滤
    filter_class = UserFilter
    # 使用UserTable展示数据
    table_class = UserTable
    template_name = 'users/user_admin.html'

    # 获取过滤后的查询集
    def get_queryset(self, **kwargs):
        qs = User.objects.all().order_by('-id')
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    # 将查询集与table实例结合，提供filter和table两个变量前端渲染
    # 每页5条记录
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t = self.table_class(data=self.get_queryset())
        RequestConfig(self.request, paginate={"per_page": 5}).configure(t)
        context['filter'] = self.filter
        context['table'] = t
        return context

    # create
    class UserCreateView(LoginRequiredMixin, CreateView):
        model = User
        template_name = 'users/user_form.html'
        form_class = UserForm
        success_url = reverse_lazy('users:user_admin')

    # update
    class UserUpdateForm(LoginRequiredMixin, UpdateView):
        model = User
        template_name = 'users/user_form.html'
        form_class = UserForm
        success_url = reverse_lazy('users:user_admin')
