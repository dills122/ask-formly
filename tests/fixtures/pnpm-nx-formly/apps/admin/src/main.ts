import { importProvidersFrom } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { FormlyModule } from '@ngx-formly/core';
import { FormlyMaterialModule } from '@ngx-formly/material';
import { FORMLY_SETUP } from '@acme/fields';
import { AdminComponent } from './app';
import { routes } from './app.routes';
bootstrapApplication(AdminComponent, { providers: [provideRouter(routes), importProvidersFrom(FormlyModule.forRoot(FORMLY_SETUP), FormlyMaterialModule)] });
