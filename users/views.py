from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile
from blog.models import Post
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"Your account has been created! You are now logged in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

class ProfileDetailView(DetailView):
    model = Profile

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        context['user_posts'] = Post.objects.filter(author=user).order_by('-date_posted')
        return context
