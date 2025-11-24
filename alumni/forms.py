from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from .models import Alumni, AlumniAddress, AcademicRecord, Career, FurtherStudy, 
from custom.models import Faculdade, Departamento, Municipality, AdministrativePost, Village, SubVillage, Nasaun, nivelmaster
# =============================
# Alumni Form
# =============================
class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = [
            'registration_no', 'name', 'sex', 'dob', 'pob',
            'father_name', 'mother_name', 'phone_number', 'email', 'photo'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('registration_no', css_class="form-group col-md-4 mb-0"),
                Column('name', css_class="form-group col-md-6 mb-0"),
                Column('sex', css_class="form-group col-md-2 mb-0"),
            ),
            Row(
                Column('dob', css_class="form-group col-md-6 mb-0"),
                Column('pob', css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column('father_name', css_class="form-group col-md-6 mb-0"),
                Column('mother_name', css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column('phone_number', css_class="form-group col-md-6 mb-0"),
                Column('email', css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column('photo', css_class="form-group col-md-12 mb-0", onchange="myFunction()"),
            ),
            HTML("""<center><img id='output' width='200'/></center>"""),
            HTML("""
                <div class="d-flex justify-content-end py-6 px-9 gap-2 mt-2">
                    <button class="btn btn-sm btn-success" type="submit">Save <i class="fa fa-save"></i></button>
                    <span class="btn btn-sm btn-danger ml-2" onclick="self.history.back()">
                        <span class="btn-label"><i class="fa fa-arrow-left"></i></span> Fila
                    </span>
                </div>
            """)
        )

# =============================
# Alumni Address Form
# =============================
class AlumniAddressForm(forms.ModelForm):
    class Meta:
        model = AlumniAddress
        fields = ['mun', 'post', 'suk', 'ald', 'detail_address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mun'].queryset = Municipality.objects.all()
        self.fields['post'].queryset = AdministrativePost.objects.none()
        self.fields['suk'].queryset = Village.objects.none()
        self.fields['ald'].queryset = SubVillage.objects.none()

        if 'mun' in self.data:
            try:
                mun_id = int(self.data.get('mun'))
                self.fields['post'].queryset = AdministrativePost.objects.filter(municipality_id=mun_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.mun:
            self.fields['post'].queryset = AdministrativePost.objects.filter(municipality=self.instance.mun)

        if 'post' in self.data:
            try:
                post_id = int(self.data.get('post'))
                self.fields['suk'].queryset = Village.objects.filter(administrativePost_id=post_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.post:
            self.fields['suk'].queryset = Village.objects.filter(administrativePost=self.instance.post)

        if 'suk' in self.data:
            try:
                suk_id = int(self.data.get('suk'))
                self.fields['ald'].queryset = SubVillage.objects.filter(village_id=suk_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.suk:
            self.fields['ald'].queryset = SubVillage.objects.filter(village=self.instance.suk)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('mun', css_class='form-group col-md-3 mb-0'),
                Column('post', css_class='form-group col-md-3 mb-0'),
                Column('suk', css_class='form-group col-md-3 mb-0'),
                Column('ald', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('detail_address', css_class='form-group col-md-12 mb-0'),
            ),
            HTML("""
                <div class="d-flex justify-content-end py-6 px-9 gap-2 mt-2">
                    <button class="btn btn-sm btn-success" type="submit">Save <i class="fa fa-save"></i></button>
                    <span class="btn btn-sm btn-danger ml-2" onclick="self.history.back()">
                        <span class="btn-label"><i class="fa fa-arrow-left"></i></span> Fila
                    </span>
                </div>
            """)
        )

# =============================
# Academic Record Form
# =============================
class AcademicRecordForm(forms.ModelForm):
    class Meta:
        model = AcademicRecord
        fields = ['faculty', 'department', 'year_start', 'year_graduation', 'thesis_title', 'advisor_1', 'advisor_2', 'gpa', 'predicate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['faculty'].queryset = Faculdade.objects.all()
        self.fields['department'].queryset = Departamento.objects.none()

        if 'faculty' in self.data:
            try:
                faculty_id = int(self.data.get('faculty'))
                self.fields['department'].queryset = Departamento.objects.filter(faculdade_id=faculty_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.faculty:
            self.fields['department'].queryset = Departamento.objects.filter(faculdade=self.instance.faculty)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('faculty', css_class='form-group col-md-6 mb-0'),
                Column('department', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('year_start', css_class='form-group col-md-3 mb-0'),
                Column('year_graduation', css_class='form-group col-md-3 mb-0'),
                Column('gpa', css_class='form-group col-md-3 mb-0'),
                Column('predicate', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('thesis_title', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('advisor_1', css_class='form-group col-md-6 mb-0'),
                Column('advisor_2', css_class='form-group col-md-6 mb-0'),
            ),
            HTML("""
                <div class="d-flex justify-content-end py-6 px-9 gap-2 mt-2">
                    <button class="btn btn-sm btn-success" type="submit">Save <i class="fa fa-save"></i></button>
                    <span class="btn btn-sm btn-danger ml-2" onclick="self.history.back()">
                        <span class="btn-label"><i class="fa fa-arrow-left"></i></span> Fila
                    </span>
                </div>
            """)
        )

# =============================
# Career Form
# =============================
class CareerForm(forms.ModelForm):
    class Meta:
        model = Career
        fields = ['job_field', 'institution', 'department', 'position', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].queryset = Nasaun.objects.all()
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('job_field', css_class='form-group col-md-4 mb-0'),
                Column('institution', css_class='form-group col-md-4 mb-0'),
                Column('department', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('position', css_class='form-group col-md-6 mb-0'),
                Column('country', css_class='form-group col-md-6 mb-0'),
            ),
            HTML("""
                <div class="d-flex justify-content-end py-6 px-9 gap-2 mt-2">
                    <button class="btn btn-sm btn-success" type="submit">Save <i class="fa fa-save"></i></button>
                    <span class="btn btn-sm btn-danger ml-2" onclick="self.history.back()">
                        <span class="btn-label"><i class="fa fa-arrow-left"></i></span> Fila
                    </span>
                </div>
            """)
        )

# =============================
# Further Study Form
# =============================
class FurtherStudyForm(forms.ModelForm):
    class Meta:
        model = FurtherStudy
        fields = ['study_level', 'major', 'university', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['study_level'].queryset = nivelmaster.objects.all()
        self.fields['country'].queryset = Nasaun.objects.all()
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('study_level', css_class='form-group col-md-3 mb-0'),
                Column('major', css_class='form-group col-md-3 mb-0'),
                Column('university', css_class='form-group col-md-3 mb-0'),
                Column('country', css_class='form-group col-md-3 mb-0'),
            ),
            HTML("""
                <div class="d-flex justify-content-end py-6 px-9 gap-2 mt-2">
                    <button class="btn btn-sm btn-success" type="submit">Save <i class="fa fa-save"></i></button>
                    <span class="btn btn-sm btn-danger ml-2" onclick="self.history.back()">
                        <span class="btn-label"><i class="fa fa-arrow-left"></i></span> Fila
                    </span>
                </div>
            """)
        )
