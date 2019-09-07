from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm,ExpenseForm
from category.forms import CategoryForm
from category.models import Category
from income.models import Income
from expenses.models import Expenses
from django.db.models import Sum
import datetime
# Create your views here.
def signup (request):
    if request.method=='GET':
        context = {
            'form':UserCreationForm(),
        }
        return render(request,'signup.html',context)
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request,'signup.html',{'form':form})


def signin(request):
    if request.method == 'GET':
        context = {
            'form': AuthenticationForm(),
        }
        return render(request, 'signin.html', context)
    else:
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u,password=p)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return redirect('signin')

@login_required(login_url='signin')
def dashboard(request):
    data = categorySum(request.user.id)
    yeardata = categorySumYear(request.user.id)
    context = {
        'data':data,
        'yeardata':yeardata
    }
    return render(request, 'dashboard.html',context)

@login_required(login_url='signin')
def income(request):
    if request.method=='GET':
        context={
            'form':IncomeForm(),
            'income':Income.objects.filter(user_id=request.user.id,date__month=getCurrentMonth(),date__year=getCurrentYear()),
            'total':Income.objects.filter(user_id=request.user.id,date__month=getCurrentMonth(),date__year=getCurrentYear()).aggregate(Sum('rupees')),
            'month':getCurrentMonth(),
            'year':getCurrentYear(),
            'previncome':getPreviousMonthData(request.user.id),
            'prevtotal':getPreviousMonthData(request.user.id).aggregate(Sum('rupees'))
        }
        return render(request,'income.html',context)
    else:
        form = IncomeForm(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            mydata = form.save(commit=False)
            mydata.user_id = request.user.id
            mydata.save()
            context.update({'msg': 'successfully added'})
        context.update({'form': form})
        return redirect('income')

@login_required(login_url='signin')
def expense(request):
    if request.method=='GET':
        context = {
            'form':ExpenseForm(request.user),
            'expenses': Expenses.objects.filter(user_id=request.user.id, date__month=getCurrentMonth(),
                                            date__year=getCurrentYear()),
            'total': Expenses.objects.filter(user_id=request.user.id, date__month=getCurrentMonth(),
                                           date__year=getCurrentYear()).aggregate(Sum('rupees')),
            'month': getCurrentMonth(),
            'year': getCurrentYear(),
            'prevexpense': getPreviousMonthExpenseData(request.user.id),
            'prevtotal': getPreviousMonthExpenseData(request.user.id).aggregate(Sum('rupees'))
        }
        return render(request,'expense.html',context)
    else:
        form = ExpenseForm(request.user,request.POST,request.FILES)
        context = {}
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            context.update({'msg':'successfully added'})
        context.update({'form':form})
        return redirect('expense')


@login_required(login_url='signin')
def income_edit(request,id):
    data = Income.objects.get(pk=id)
    form = IncomeForm(request.POST or None, request.FILES or None,instance=data)
    if form.is_valid():
        form.save()
        return redirect('income')
    context = {
        'form':form
    }
    return render(request,'income_edit.html',context)

@login_required(login_url='signin')
def expenses_edit(request,id):
    data = Expenses.objects.get(pk=id)
    form = ExpenseForm(request.user,request.POST or None, request.FILES or None,instance=data)
    if form.is_valid():
        form.save()
        return redirect('expense')
    context = {
        'form':form
    }
    return render(request,'expense_edit.html',context)

@login_required(login_url='signin')
def income_delete(request,id):
    income = Income.objects.get(pk=id)
    income.delete()
    return redirect('income')

@login_required(login_url='signin')
def expenses_delete(request,id):
    expenses = Expenses.objects.get(pk=id)
    expenses.delete()
    return redirect('expense')

@login_required(login_url='signin')
def category(request):
    if request.method=='GET':
        context = {
            'form' : CategoryForm(),
            'category':Category.objects.filter(user_id=request.user.id)

        }
        return render(request,'category.html',context)
    else:
        form = CategoryForm(request.POST)
        if form.is_valid():
            data  = form.save(commit=False)
            data.user_id = request.user.id
            data.save()
            return redirect('category')
        return render(request,'category.html',{'form':form})

def my_logout(request):
    logout(request)
    return redirect('signin')


def getCurrentMonth():
    return datetime.date.today().month
def getCurrentYear():
    return datetime.date.today().year


def getPreviousMonthData(id):
    today_month = datetime.date.today().month
    today_year = datetime.date.today().year

    if today_month != 1:
        previous_month = today_month-1
        previous_month_year = today_year
    else:
        previous_month=12
        previous_month_year=today_year-1
    return Income.objects.filter(user_id=id,date__month=previous_month,date__year=previous_month_year)

def getPreviousMonthExpenseData(id):
    today_month = datetime.date.today().month
    today_year = datetime.date.today().year

    if today_month != 1:
        previous_month = today_month-1
        previous_month_year = today_year
    else:
        previous_month=12
        previous_month_year=today_year-1
    return Expenses.objects.filter(user_id=id,date__month=previous_month,date__year=previous_month_year)


def categorySum(id):
    all_category = Category.objects.filter(user_id=id)
    category_label = []
    category_sum = []
    for x in all_category:
        exp = Expenses.objects.filter(user_id=id,date__month=getCurrentMonth(),date__year=getCurrentYear(),category_id=x.id).aggregate(Sum('rupees'))
        if exp['rupees__sum'] is not None:
            total = exp['rupees__sum']
        else:
            total = 0
        category_label.append(x.title)
        category_sum.append(total)
    return list(zip(category_label,category_sum))

def categorySumYear(id):
    all_category = Category.objects.filter(user_id=id)
    category_label = []
    category_sum = []
    for x in all_category:
        exp = Expenses.objects.filter(user_id=id,date__year=getCurrentYear(),category_id=x.id).aggregate(Sum('rupees'))
        if exp['rupees__sum'] is not None:
            total = exp['rupees__sum']
        else:
            total = 0
        category_label.append(x.title)
        category_sum.append(total)
    return list(zip(category_label,category_sum))