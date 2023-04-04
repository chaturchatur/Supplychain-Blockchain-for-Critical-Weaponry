from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, FormView,DetailView,TemplateView 
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from .models import Indent, Part
from .forms import Order, Part_Entity
from accounts.models import Account
from django.conf import settings
from datetime import datetime
from web3 import Web3

class IndentListView(ListView):
    template_name = 'home.html'
    def get_queryset(self):
        user = self.request.user
        return Indent.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        account = Account.objects.get(user=self.request.user)
        acct = settings.WEB3.eth.account.privateKeyToAccount(account.privatekey)
        context['account'] = acct.address
        return context

class IndentView(FormView):
    template_name = 'indent.html'
    form_class = Order
    def get_success_url(self):
        return '/indent/' + self.kwargs['id']
    def get_context_data(self,**kwargs):
        indent_record = Indent.objects.get(pk=self.kwargs['id'])
        context = super().get_context_data(**kwargs)
        account = Account.objects.get(user=self.request.user)
        w3 = settings.WEB3
        acct = w3.eth.account.privateKeyToAccount(account.privatekey)
        indent = w3.eth.contract(abi=settings.INDENT_ABI,address='0x' + indent_record.address)
        context['indent'] = indent_record
        context['owner'] = indent.functions.owner().call()
        context['creator'] = indent.functions.creator().call()
        context['creation_date'] = datetime.fromtimestamp(indent.functions.creation_date().call())
        context['reviser'] = indent.functions.reviser().call()
        context['revision_date'] = datetime.fromtimestamp(indent.functions.modify_date().call())
        context['account'] = acct.address
        context['orders'] = indent.functions.get_part_orders().call()
        return context
    
    def form_valid(self,form):
        indent_record = Indent.objects.get(pk=self.kwargs['id'])
        account = Account.objects.get(user=self.request.user)
        w3 = settings.WEB3
        acct = w3.eth.account.privateKeyToAccount(account.privatekey)
        indent = w3.eth.contract(abi=settings.INDENT_ABI,address='0x' + indent_record.address)
        indent.functions.add_edit_order(str(form.cleaned_data['part_id']),form.cleaned_data['dues_out'],form.cleaned_data['dues_in']).transact({'from':acct.address})
        return redirect('/indent/'+self.kwargs['id'])




@require_http_methods(['GET'])
def CreateIndentView(request):
    account = Account.objects.get(user=request.user)
    w3 = settings.WEB3
    acct = w3.eth.account.privateKeyToAccount(account.privatekey)
    indent = w3.eth.contract(abi=settings.INDENT_ABI, bytecode=settings.INDENT_BYTECODE)
    tx_hash = indent.constructor(True).transact({'from':acct.address})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    indent_record = Indent.objects.create(owner=request.user,address=tx_receipt.contractAddress[2:])
    return redirect('/indent/'+str(indent_record.id))

class PartView(DetailView):
    model = Part
    template_name = 'part.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = Account.objects.get(user=self.request.user)
        w3 = settings.WEB3
        acct = w3.eth.account.privateKeyToAccount(account.privatekey)
        context['account'] = acct.address
        return context

class RegisterPart(FormView):
    template_name = 'register.html'
    form_class = Part_Entity
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = Account.objects.get(user=self.request.user)
        w3 = settings.WEB3
        acct = w3.eth.account.privateKeyToAccount(account.privatekey)
        context['account'] = acct.address
        return context

    def form_valid(self, form):
        indent_record = Indent.objects.get(pk=form.cleaned_data['indent'])
        account = Account.objects.get(user=self.request.user)
        w3 = settings.WEB3
        acct = w3.eth.account.privateKeyToAccount(account.privatekey)
        indent = w3.eth.contract(abi=settings.INDENT_ABI,address='0x' + indent_record.address)
        part_contract = indent.functions.register_part(form.cleaned_data['entity_id'],str(form.cleaned_data['part_id']),form.cleaned_data['status'],form.cleaned_data['location'],form.cleaned_data['maintentance_status']).call()
        indent.functions.register_part(form.cleaned_data['entity_id'],str(form.cleaned_data['part_id']),form.cleaned_data['status'],form.cleaned_data['location'],form.cleaned_data['maintentance_status']).transact({'from':acct.address})
        return redirect('/entity/'+part_contract[2:])

class ViewEntity(TemplateView):
    template_name = 'entity.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = Account.objects.get(user=self.request.user)
        w3 = settings.WEB3
        acct = w3.eth.account.privateKeyToAccount(account.privatekey)
        part = w3.eth.contract(abi=settings.PART_ABI,address='0x' + self.kwargs['entity_hash'])
        context['entity_id'] = part.functions.entity_id().call()
        context['part_id'] = part.functions.part_id().call()
        context['status'] = part.functions.current_status().call()
        context['location'] = part.functions.current_loc().call()
        context['handler'] = part.functions.current_handler().call()
        context['indent'] = part.functions.indent().call()
        context['entity_id'] = part.functions.entity_id().call()
        context['maintenance_status'] = part.functions.maintenance_status().call()
        context['account'] = acct.address
        return context



   