rom django.conf.urls import patterns, include, url
from django.views.generic import *
from backoffice.models import *
from django import forms
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

ProductItemFormSet = inlineformset_factory(Product, ProductItem)

class ProductCreateView(CreateView):

    form_class = ProductForm
    model = Product
    success_url = "/product/new/"
    
    def get(self, request, *args, **kwargs):
        
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        product_item_form = ProductItemFormSet()
        return self.render_to_response(self.get_context_data(form=form, product_item_form=product_item_form))
    
    def post(self, request, *args, **kwargs):
      
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        product_item_form = ProductItemFormSet(self.request.POST)
         
        if form.is_valid() and product_item_form.is_valid():
            return self.form_valid(form, product_item_form)
        else:
            return self.form_invalid(form, product_item_form)
        
    def form_valid(self, form, product_item_form):
        
        self.object = form.save()
        product_item_form.instance = self.object
        product_item_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, product_item_form):
        
        return self.render_to_response(self.get_context_data(form=form, product_item_form=product_item_form))

urlpatterns = patterns('',
    url(r'^product/new/$', ProductCreateView.as_view()),
)