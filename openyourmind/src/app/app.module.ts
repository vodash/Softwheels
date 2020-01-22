import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {LoginComponent} from './login/login.component';
import {MenuComponent} from './menu/menu.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {ChartComponent} from './chart/chart.component';
import {HighchartsChartComponent} from 'highcharts-angular';
import { DoctorProfileComponent } from './doctor-profile/doctor-profile.component';
import { PatientProfileComponent } from './patient-profile/patient-profile.component';
import { PatientOverviewComponent } from './patient-overview/patient-overview.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import {AuthGuardService} from './authentication/auth-guard.service';
import {LoginAuthGuardService} from "./authentication/auth-guard-login.service";
import { PatientCreationComponent } from './patient-creation/patient-creation.component';
import { AdminMenuComponent } from './admin-menu/admin-menu.component';
import { PasswordresetComponent } from './adminPages/passwordreset/passwordreset.component';
import { UserOverviewComponent } from './adminPages/user-overview/user-overview.component';
import { PatientListComponent } from './secretary-pages/patient-list/patient-list.component';
import { SecretaryMenuComponent } from './secretary-menu/secretary-menu.component';
import { TherapistsComponent } from './secretary-pages/therapists/therapists.component';
import { TherapistPatientsListComponent } from './secretary-pages/therapist-patients-list/therapist-patients-list.component';



@NgModule({
    declarations: [
        AppComponent,
        LoginComponent,
        MenuComponent,
        ChartComponent,
        HighchartsChartComponent,
        DoctorProfileComponent,
        PatientProfileComponent,
        PatientOverviewComponent,
        PatientCreationComponent,
        AdminMenuComponent,
        PasswordresetComponent,
        UserOverviewComponent,
        PatientListComponent,
        SecretaryMenuComponent,
        TherapistsComponent,
        TherapistPatientsListComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        BrowserAnimationsModule,
        NgbModule,
        ReactiveFormsModule,
        FormsModule,
        HttpClientModule


    ],
    providers: [AuthGuardService, LoginAuthGuardService],
    bootstrap: [AppComponent]
})
export class AppModule {

}
