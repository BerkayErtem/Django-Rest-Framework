
from django.db.models import fields
from rest_framework import serializers
from .models import User, Company, Subsidiary, Image, Form
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model=Form
        fields='__all__'
        extra_kwargs={'id':{'read_only':True},
                        'approval':{'read_only':True}}
    def save(self):
        form=Form(

            destination=self.validated_data['destination'],
            date=self.validated_data['date']
        )
        form.save()
        return form

class userSerializer(serializers.HyperlinkedModelSerializer):

    password2=serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model=User
        fields= ['username', 'password', 'password2','id','company_name', 'phone']
        extra_kwargs={'password':{'write_only':True},
                    'company_name':{'read_only':True},
                    'phone':{'read_only':True}}
    
    def save(self):
        user=User(
            username=self.validated_data['username'],
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']

        if password!=password2:
            raise serializers.ValidationError({'password':'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class updateForm(serializers.ModelSerializer):
    class Meta:
        model=Form
        fields='__all__' 
        extra_kwargs={'destination': {'required': False},'date': {'required': False}}
        def update(self, instance, validated_data):
            instance.approval=self.validated_data['approval']
            instance.destination=self.validated_data['destination']
            instance.save() 
            return instance
class updateUser(serializers.ModelSerializer):
    
    class Meta:
        model=User
        # fields=('username','is_staff','company_name','is_admin')
        fields='__all__'
        extra_kwargs = {'username': {'required': False},'password': {'required': False},'is_admin': {'required': False}} 
        

    def update(self, instance, validated_data):
        method=self.context['request'].method
        auth=self.context['request'].auth
        user=self.context['request'].user

        instance.username=self.validated_data['username']
        instance.is_admin=self.validated_data['is_admin']
        instance.is_staff=self.validated_data['is_staff']
        instance.company_name=self.validated_data['company_name'] 
        
        if user.pk!= instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        print(method)
        print(auth)
        print(user.username)
        print(user.pk)
        instance.save() 
        return instance

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Company
        fields='__all__'
    def save(self):
        company=Company(

            companyTitle=self.validated_data['companyTitle'],
            companyName=self.validated_data['companyName'],
            taxOffice=self.validated_data['taxOffice'],
            taxNumber=self.validated_data['taxNumber'],
            tel=self.validated_data['tel'],
            email=self.validated_data['email'],
            address=self.validated_data['address'],
        )
        company.save()
        return company
class subsidiarySerializer(serializers.ModelSerializer):
    class Meta:
        model=Subsidiary
        fields='__all__'

    def save(self):
        
        subsidiary=Subsidiary(
            companyName=self.validated_data['companyName'],
            subsidiaryTitle=self.validated_data['subsidiaryTitle'],
            subsidiaryName=self.validated_data['subsidiaryName'],
            sub_taxNumber=self.validated_data['sub_taxNumber'],
            sub_tel=self.validated_data['sub_tel'],
            sub_email=self.validated_data['sub_email'],
            sub_taxOffice=self.validated_data['sub_taxOffice'],
            sub_address=self.validated_data['sub_address'] 
            
        )
        subsidiary.save()
        return subsidiary

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class imageSerializer(serializers.ModelSerializer):
    image=serializers.ImageField(max_length=200, use_url=True)
    
    class Meta:
        model=Image
        fields='__all__'

    def save(self):
        
        image=Image(
            image_name=self.validated_data['image_name'],
            image=self.validated_data['image'],
            
        )
        image.save()
        return image
