from rest_framework import fields, serializers
from users.models import NewUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = NewUser
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance




class NewUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """

    class Meta:
        model = NewUser
        fields = ('id','email','username','first_name','start_date','about')



    #     email = models.EmailField(_('email address'), unique=True)
    # username = models.CharField(max_length=150, unique=True)
    # first_name = models.CharField(max_length=150, blank=True)
    # start_date = models.DateTimeField(default=timezone.now)
    # about = models.TextField(_(
    #     'about'), max_length=500, blank=True)
    # is_staff = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)