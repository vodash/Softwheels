import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {LoginComponent} from './login/login.component';
import {ChartComponent} from './chart/chart.component';
import {DoctorProfileComponent} from './doctor-profile/doctor-profile.component';
import {PatientProfileComponent} from './patient-profile/patient-profile.component';
import {PatientOverviewComponent} from "./patient-overview/patient-overview.component";

// router module for navigation in the web app
const routes: Routes = [
    {
        path: '',
        component: LoginComponent
    },
    {
        path: 'chart',
        component: ChartComponent
    },
    {
        path: 'profile',
        component: DoctorProfileComponent
    },
    {
        path: 'patient',
        component: PatientProfileComponent
    },{
        path: 'patientOverview',
        component: PatientOverviewComponent
    }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
