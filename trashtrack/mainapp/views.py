from django.shortcuts import render, redirect, get_object_or_404
from .models import SmartBin, Vehicle, DumpingArea, Company
from .forms import CompanySignupForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


# Function to add common context (bin notifications) to every view
def common_context(request):
    # Get bins that have a fill level greater than 70%
    bins_over_70 = SmartBin.objects.filter(current_fill_level__gt=70)
    return {
        "bin_notifications": bins_over_70  # bins with fill levels greater than 70%
    }

# Login view
def login_view(request):
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

# Company signup view
def company_signup(request):
    if request.user.is_authenticated:
        return redirect('company_portal')

    if request.method == 'POST':
        form = CompanySignupForm(request.POST)
        if form.is_valid():
            company_profile = form.save()
            login(request, company_profile.user)
            return redirect('company_portal')
    else:
        form = CompanySignupForm()
    return render(request, 'company_signup.html', {'form': form})

# Dashboard view to show all key data with notifications for bins over 70% full
@login_required
def dashboard(request):
    context = common_context(request)
    context.update({
        "bins": SmartBin.objects.all(),
        "vehicles": Vehicle.objects.all(),
        "waste_types": DumpingArea.objects.all(),
    })
    return render(request, "dashboard.html", context)

# Map view to show bins' locations
@login_required
def map_view(request):
    bins = list(SmartBin.objects.values('bin_type', 'current_fill_level', 'location', 'latitude', 'longitude'))
    return render(request, "map.html", {"bins": bins})

# Smart Bins view
@login_required
def smart_bins(request):
    context = common_context(request)
    bins = SmartBin.objects.all()
    context.update({"bins": bins})
    return render(request, "smart_bins.html", context)

# Update fill level for a Smart Bin
@login_required
def update_bin_fill_level(request, bin_id):
    bin = get_object_or_404(SmartBin, id=bin_id)
    if request.method == 'POST':
        new_fill_level = request.POST.get('current_fill_level')
        if new_fill_level.isdigit() and 0 <= int(new_fill_level) <= 100:
            bin.current_fill_level = int(new_fill_level)
            bin.save()  
            return HttpResponseRedirect(reverse('smart_bins'))  
    return render(request, "update_bin.html", {"bin": bin})

# Tracking and Collection view
@login_required
def tracking(request):
    context = common_context(request)
    vehicles = Vehicle.objects.all()
    context.update({"vehicles": vehicles})
    return render(request, "tracking.html", context)

# Dumping Area Management view
@login_required
def dumping_area(request):
    context = common_context(request)
    waste_types = DumpingArea.objects.all()
    context.update({"waste_types": waste_types})
    return render(request, "dumping_area.html", context)

# Company Portal view
@login_required
def company_portal(request):
    context = common_context(request)
    companies = Company.objects.all()
    context.update({"companies": companies})
    return render(request, "company_portal.html", context)
