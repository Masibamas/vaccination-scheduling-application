from django.shortcuts import render
from vaccine.models import Vaccine
from django.views import generic
from campaign.models import Campaign, Slot
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from vaccination.forms import VaccinationForm
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from vaccination.models import Vaccination
from vaccination.utils import generate_pdf
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse


class ChooseVaccine(LoginRequiredMixin, generic.ListView):
    model = Vaccine
    template_name = "vaccination/choose-vaccine.html"
    paginate_by = 10
    ordering = ["name"]

class ChooseCampaign(LoginRequiredMixin, generic.ListView):
    model = Campaign
    template_name = "vaccination/choose-campaign.html"
    paginate_by = 10
    ordering = ["start_date"]

    def get_queryset(self):
        return super().get_queryset().filter(vaccine = self.kwargs["vaccine_id"])
    
class ChooseSlot(LoginRequiredMixin, generic.ListView):
    model = Slot
    template_name = "vaccination/choose-slot.html"
    paginate_by = 10
    ordering = ["date"]

    def get_queryset(self):
        return super().get_queryset().filter(campaign = self.kwargs["campaign_id"], date__gte = timezone.now())
    

class ConfirmVaccination(View):
    form_class = VaccinationForm

    def get(self, request, *args, **kwargs):
        campaign = Campaign.objects.get(id = self.kwargs["campaign_id"])
        slot = Slot.objects.get(id = self.kwargs["slot_id"])
        form = self.form_class(initial={
            "patient": request.user,
            "campaign":campaign,
            "slot":slot,
        })
        context = {
            "patient":request.user, 
            "campaign":campaign,
            "slot":slot,
            "form": form,
        }
        return render(request, "vaccination/confirm-vaccination.html", context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            is_reserved = Slot.reserve_vaccine(self.kwargs["campaign_id"], self.kwargs["slot_id"])
            if is_reserved:
                form.save()
                return HttpResponse("Your Vaccination had been scheduled")
            return HttpResponseBadRequest("Unable to reserve vaccine at this moment ")
        return HttpResponseBadRequest("invalid Form Data")

class VaccinationList(LoginRequiredMixin, generic.ListView):
    model = Vaccination
    template_name = "vaccination/vaccination-list.html"
    paginate_by = 10
    ordering = ["id"]

    def get_queryset(self):
        return super().get_queryset().filter(patient = self.request.user)

class VaccinationDetail(LoginRequiredMixin, generic.DetailView):
    model = Vaccination
    template_name = "vaccination/vaccination-detail.html"
@login_required
def appointment_letter(request, vaccination_id):
    vaccination=Vaccination.objects.get(id=vaccination_id)
    context = {
        "pdf_title":f"{vaccination.patient.get_full_name()} | Appointment Letter", 
        "date": str(timezone.now()),
        "title":"Appointment Letter",
        "subtitle":"To whom it may concern",
        "content": f" This is to inform that the {vaccination.campaign.vaccine.name} vaccination of Mr/Mrs {vaccination.patient.get_full_name()} is scheduled on {vaccination.slot.date}"
    }
    return generate_pdf(context)
@login_required
def vaccination_certificate(request, vaccination_id):
    vaccination = Vaccination.objects.get(id=vaccination_id)
    if vaccination.is_vaccinated:
        context = {
                "pdf_title": f"{vaccination.patient.get_full_name()} | Vaccination Certificate",
                "date": str(timezone.now()),
                "title": "Vaccination Certificate",
                "subtitle": "To whom it may concerns", 
                "content": f"This is to certify that MR/Mrs {vaccination.patient.get_full_name()} has successfully taken {vaccination.campaign.vaccine.name} on {vaccination.date}. The vaccination was scheduled on {vaccination.slot.date} {vaccination.slot.start_time} at {vaccination.campaign.center.name}."
        }
        return generate_pdf(context)
    return HttpResponseBadRequest("User is not vaccinated")

def approve_vaccination(request, vaccination_id):
    if request.user.has_perm("vaccination.change_vaccination"):
        try:
            vaccination = Vaccination.objects.get(id=vaccination_id)
        except Vaccination.DoesNotExist:
            return HttpResponseBadRequest("Vaccination with the given object id doesnot exist")
        
        if request.user in vaccination.campaign.agents.all():
            if vaccination.is_vaccinated:
                return HttpResponse("Petient is already vaccinated")
            vaccination.is_vaccinated = True
            vaccination.date = timezone.now()
            vaccination.updated_by = request.user
            vaccination.save()
            return HttpResponseRedirect(reverse("vaccination:vaccination-detail", kwargs={"pk": vaccination_id}))
        raise PermissionDenied()
    raise PermissionDenied()