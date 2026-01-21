from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .forms import TicketForm, UserRegisterForm, CommentForm
from .models import Ticket, UserProfile, User, Comment

# --- DASHBOARDS ---
@login_required
def dashboard(request):
    user = request.user
    if not hasattr(user, 'userprofile'): return render(request, 'home.html')
    if not user.is_superuser and not user.userprofile.is_approved: return render(request, 'dashboards/pending_approval.html')
    
    role = user.userprofile.role
    if role == 'ADMIN': return admin_dashboard(request)
    elif role == 'ENGINEER': return engineer_dashboard(request)
    else: return user_dashboard(request)

def user_dashboard(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'dashboards/user_dashboard.html', {'tickets': tickets})

def engineer_dashboard(request):
    tickets = Ticket.objects.filter(assigned_to=request.user).exclude(status='Resolved').order_by('-created_at')
    return render(request, 'dashboards/engineer_dashboard.html', {'tickets': tickets})

def admin_dashboard(request):
    tickets = Ticket.objects.all().order_by('-created_at')
    pending_users = UserProfile.objects.filter(is_approved=False)
    engineers = User.objects.filter(userprofile__role='ENGINEER', userprofile__is_approved=True)

    # --- ANALYTICS DATA ---
    # Count tickets by Status
    status_counts = Ticket.objects.values('status').annotate(count=Count('status'))
    status_data = {item['status']: item['count'] for item in status_counts}
    
    # Count tickets by Priority
    priority_counts = Ticket.objects.values('priority').annotate(count=Count('priority'))
    priority_data = {item['priority']: item['count'] for item in priority_counts}

    context = {
        'tickets': tickets,
        'pending_users': pending_users,
        'engineers': engineers,
        'open_tickets': tickets.filter(status='Open').count(),
        'resolved_tickets': tickets.filter(status='Resolved').count(),
        # Pass Data to Template
        'status_labels': list(status_data.keys()),
        'status_values': list(status_data.values()),
        'priority_labels': list(priority_data.keys()),
        'priority_values': list(priority_data.values()),
    }
    return render(request, 'dashboards/admin_dashboard.html', context)

# --- TICKET & COMMENTS ---
@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Security Check: Only allow Owner, Assigned Engineer, or Admin
    if request.user != ticket.created_by and request.user != ticket.assigned_to and request.user.userprofile.role != 'ADMIN' and not request.user.is_superuser:
        messages.error(request, "Access Denied")
        return redirect('dashboard')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            messages.success(request, "Reply posted.")
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = CommentForm()

    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket, 'form': form})

# --- ACTIONS ---
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, "Ticket created.")
            return redirect('dashboard')
    else:
        form = TicketForm()
    return render(request, 'tickets/create_ticket.html', {'form': form})

@login_required
def assign_ticket(request, ticket_id):
    if request.user.userprofile.role != 'ADMIN' and not request.user.is_superuser:
        return redirect('dashboard')
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        eng_id = request.POST.get('engineer_id')
        if eng_id:
            ticket.assigned_to_id = eng_id
            ticket.status = 'In Progress'
            ticket.save()
            messages.success(request, "Assigned.")
    return redirect('dashboard')

@login_required
def update_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.assigned_to != request.user: return redirect('dashboard')
    if request.method == 'POST':
        new_status = request.POST.get('status')
        ticket.status = new_status
        ticket.save()
    return redirect('dashboard')

@login_required
def approve_user(request, profile_id):
    if not request.user.is_superuser: return redirect('dashboard')
    profile = get_object_or_404(UserProfile, id=profile_id)
    profile.is_approved = True
    profile.save()
    return redirect('dashboard')

# --- PUBLIC ---
def home(request):
    if request.user.is_authenticated: return redirect('dashboard')
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user.userprofile.role = form.cleaned_data['role']
            user.userprofile.save()
            messages.success(request, "Account created! Wait for approval.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/signup.html', {'form': form})