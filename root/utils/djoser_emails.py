from djoser import email


class ActivationEmail(email.ActivationEmail):
    template_name = 'emails/activation_mail.html'

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["confirm_code"] = user.confirm_code
        return context


class ConfirmationEmail(email.ConfirmationEmail):
    template_name = 'emails/confirmation_email.html'


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "emails/password_reset_email.html"


class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = "emails/password_changed_confirmation_email.html"
