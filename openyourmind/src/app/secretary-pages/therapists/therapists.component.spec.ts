import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TherapistsComponent } from './therapists.component';

describe('TherapistsComponent', () => {
  let component: TherapistsComponent;
  let fixture: ComponentFixture<TherapistsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TherapistsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TherapistsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
