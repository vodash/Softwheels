import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SecretaryMenuComponent } from './secretary-menu.component';

describe('SecretaryMenuComponent', () => {
  let component: SecretaryMenuComponent;
  let fixture: ComponentFixture<SecretaryMenuComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SecretaryMenuComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SecretaryMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
