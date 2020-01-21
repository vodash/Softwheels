import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {LoginComponent} from './login/login.component';
import {ChartComponent} from './chart/chart.component';
import {DoctorProfileComponent} from './doctor-profile/doctor-profile.component';
import {PatientProfileComponent} from './patient-profile/patient-profile.component';
import {PatientOverviewComponent} from './patient-overview/patient-overview.component';
import {AuthGuardService as AuthGuard} from './authentication/auth-guard.service';
import {LoginAuthGuardService as LoginAuthGuard} from './authentication/auth-guard-login.service';
import {PatientCreationComponent} from './patient-creation/patient-creation.component';
import { PasswordresetComponent } from './adminPages/passwordreset/passwordreset.component';
import { UserOverviewComponent } from './adminPages/user-overview/user-overview.component';
import { PatientListComponent } from './secretary-pages/patient-list/patient-list.component';

// router module for navigation in the web app
const routes: Routes = [
    {
        path: '',
        component: LoginComponent,
        canActivate: [LoginAuthGuard]
    },
    {
        path: 'chart',
        component: ChartComponent,
        canActivate: [AuthGuard]
    },
    {
        path: 'profile',
        component: DoctorProfileComponent
    },
    {
        path: 'patient',
        component: PatientProfileComponent
    },
    {
        path: 'patient-overview',
        component: PatientOverviewComponent
    },
    {
        path: 'patient-creation',
        component: PatientCreationComponent
    },
    {   path: 'reset-password',
        component: PasswordresetComponent
    },
    {   path: 'user-overview',
        component: UserOverviewComponent
    },
    {
        path: 'all-patients-list',
        component: PatientListComponent
    }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
