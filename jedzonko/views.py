import random
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from django.views import View
from jedzonko.models import *


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


def landing_page(request):
    recipes = random.sample(list(Recipe.objects.all()), 3)
    counter_plans = Plan.objects.count()
    counter_recipes = Recipe.objects.count()
    plan=Plan.objects.order_by('-created')
    DayName.objects.order_by('-order')
    plan = plan.first()
    rec_plan = RecipePlan.objects.filter(plan_id=plan)
    days_names = [1, 2, 3, 5, 6, 7, 8]
    recipes_for_week = {}
    for day in days_names:
        recipes_plan = RecipePlan.objects.filter(day_name=day, plan=plan)
        recipes_for_week[day] = recipes_plan
    recipes_for_week['Poniedziałek'] = recipes_for_week.pop(1)
    recipes_for_week['Wtorek'] = recipes_for_week.pop(2)
    recipes_for_week['Środa'] = recipes_for_week.pop(3)
    recipes_for_week['Czwartek'] = recipes_for_week.pop(5)
    recipes_for_week['Piątek'] = recipes_for_week.pop(6)
    recipes_for_week['Sobota'] = recipes_for_week.pop(7)
    recipes_for_week['Niedziela'] = recipes_for_week.pop(8)
    return render(request, 'index.html', context={'recipes': recipes,
                                                                  "counter_recipes": counter_recipes,
                                                                  "counter_plans": counter_plans,
                                                                  "plan": plan,
                                                                  'rec_plan': rec_plan,
                                                                  'days_names': days_names,
                                                                  'recipes_for_week': recipes_for_week})


def render_about(request):
    try:
        if Page.objects.get(slug='about'):
            about = Page.objects.get(slug='about')
            return render(request, 'app-about.html', context={'about': about})
    except:
        return HttpResponse('Strona w przygotowaniu.')


def render_contact(request):
    try:
        if Page.objects.get(slug='contact'):
            contact = Page.objects.get(slug='contact')
            return render(request, 'app-contact.html', context={'contact': contact})
    except:
        return HttpResponse('Strona w przygotowaniu.')


class NewRecipe(View):
    def get(self, request):
        return render(request, 'app-add-recipe.html')

    def post(self, request):
        name = request.POST.get('name').strip()
        description = request.POST.get('description')
        time = request.POST.get('time')
        preparation = request.POST.get('preparation')
        ingredients = request.POST.get('ingredients')
        if name != "" and description != "" and int(time) > 0 and preparation != "" and ingredients != "":
            if len(Recipe.objects.filter(name=name)) > 0:
                error = "Taki przepis już istnieje"
                return render(request, 'app-add-recipe.html', context={'error': error})
            else:
                Recipe.objects.create(name=name, description=description, preparation_time=time,
                                      preparation=preparation, ingredients=ingredients)
                return redirect('/recipe/list')
        else:
            error = "Wypełnij wszystkie pola"
            return render(request, 'app-add-recipe.html', context={'error': error})


def render_recipe_list(request):
    all_recipes = Recipe.objects.all().order_by('-votes', '-created')
    paginator = Paginator(all_recipes, 50)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    return render(request, 'app-recipes.html', context={'recipes': recipes})


def plan_list(request):
    all_plans = Plan.objects.all().order_by('name', '-created')
    paginator = Paginator(all_plans, 50)
    page = request.GET.get('page')
    plans = paginator.get_page(page)
    return render(request, 'app-schedules.html', context={'plans': plans})


class RecipeDetails(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(pk=id)
        punctuation = [',', '.', ';', '/']
        splitter = 'not-a-mark'
        for mark in punctuation:
            if mark in recipe.ingredients:
                splitter = mark
        if splitter in recipe.ingredients:
            ingredients = recipe.ingredients.split(splitter)
        else:
            ingredients = recipe.ingredients.splitlines()
        return render(request, 'app-recipe-details.html',
                      context={'recipe': recipe, 'ingredients': ingredients, 'id': id})

    def post(self, request, id):
        pk = request.POST.get('post_id')
        action = request.POST.get('action')
        recipe = Recipe.objects.get(pk=pk)
        if action == 'like':
            recipe.votes += 1
            recipe.save()
        elif action == 'dislike':
            recipe.votes -= 1
            recipe.save()
        return redirect(f'/recipe/{pk}')


class EditRecipe(View):
    def get(self, request, id):
        try:
            recipe = Recipe.objects.get(pk=id)
        except Recipe.DoesNotExist:
            raise Http404('Recipe does not exist')
        return render(request, 'app-edit-recipe.html', context={'recipe': recipe})

    def post(self, request, id):
        name = request.POST.get('name')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        preparation = request.POST.get('preparation')
        ingredients = request.POST.get('ingredients')
        if name == '' or description == '' or preparation_time == '' or preparation == '' or ingredients == '':
            messages.warning(request, 'Wypełnij poprawnie wszystkie pola')
            return redirect(f'/recipe/modify/{id}')
        else:
            Recipe.objects.create(name=name, description=description,
                                  preparation_time=preparation_time,
                                  preparation=preparation, ingredients=ingredients)
            return redirect(f'/recipe/list')


def schedules(request):
    return render(request, 'app-schedules.html')


class RenderPlanAdd(View):
    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        name = request.POST.get('planName')
        description = request.POST.get('planDescription')
        if name != "" or description != "":
            plan = Plan.objects.create(name=name, description=description)
            request.session['plan_id'] = plan.pk
            return redirect('/plan/add')
        else:
            error = "Wypełnij wszystkie pola"
            return render(request, 'app-add-schedules.html', context={'error': error})


def plan_details(request, id):
    plan = Plan.objects.get(pk=id)
    rec_plan = RecipePlan.objects.filter(plan_id=plan)
    days_names = [1, 2, 3, 5, 6, 7, 8]
    recipes_for_week = {}
    for day in days_names:
        recipes_plan = RecipePlan.objects.filter(day_name=day, plan=plan)
        recipes_for_week[day] = recipes_plan
    recipes_for_week['Poniedziałek'] = recipes_for_week.pop(1)
    recipes_for_week['Wtorek'] = recipes_for_week.pop(2)
    recipes_for_week['Środa'] = recipes_for_week.pop(3)
    recipes_for_week['Czwartek'] = recipes_for_week.pop(5)
    recipes_for_week['Piątek'] = recipes_for_week.pop(6)
    recipes_for_week['Sobota'] = recipes_for_week.pop(7)
    recipes_for_week['Niedziela'] = recipes_for_week.pop(8)
    return render(request, 'app-details-schedules.html', context={'plan': plan,
                                                                  'rec_plan': rec_plan,
                                                                  'days_names': days_names,
                                                                  'recipes_for_week': recipes_for_week})


class RenderPlanAddDetails(View):
    def get(self, request):
        if request.session.get("plan_id") is None:
            return HttpResponse('brak plan_it', status=403)
        else:
            recipes = Recipe.objects.all()
            plans = Plan.objects.all()
            days = DayName.objects.all()
            return render(request, 'app-schedules-meal-recipe.html', context={"plans": plans,
                                                                              "recipes": recipes,
                                                                              "days": days})

    def post(self, request):
        def del_sesion_plan_id(request):
            if (request.POST.get('delete_ses_plan_id')):
                request.session['plan_id'] = None
                return redirect('/plan/list/')

        recipe_pk = Recipe.objects.get(pk=int(request.POST.get("recipe_pk")))
        plan_pk = Plan.objects.get(pk=int(request.POST.get("plan_pk")))
        meal_order = request.POST.get("meal_order")
        meal_name = request.POST.get("meal_name")
        day_pk = DayName.objects.get(pk=int(request.POST.get("day_pk")))
        if plan_pk.pk == request.session.get("plan_id"):
            RecipePlan.objects.create(recipe=recipe_pk, plan=plan_pk, day_name=day_pk, meal_name=meal_name,
                                      order=meal_order)
            del_sesion_plan_id(request)
            return RenderPlanAddDetails.get(self, request)
        else:
            raise Http404(f"nie ma takiej strony {type(plan_pk.pk)} :: {type(request.session.get('plan_id'))}")
