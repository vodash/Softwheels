import { Component, OnInit } from '@angular/core';
import {AuthService} from "../authentication/authService";

@Component({
  selector: 'app-doctor-profile',
  templateUrl: './doctor-profile.component.html',
  styleUrls: ['./doctor-profile.component.css']
})
export class DoctorProfileComponent implements OnInit {

  constructor(private authService: AuthService
  ) {}

  ngOnInit() {
  }
  test() {
      this.authService.GetuserID()
          .subscribe(
              () => {
                  console.log("work pls");
              }
          );
  }

}
