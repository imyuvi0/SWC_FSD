import { Routes } from '@angular/router';
import { GameListComponent } from './components/game-list/game-list.component';
import { GameDetailComponent } from './components/game-detail/game-detail.component';
import { AddGameFormComponent } from './components/add-game-form/add-game-form.component';

export const routes: Routes = [
  // Default route: redirects empty path to the catalog list page
  { path: '', redirectTo: 'games', pathMatch: 'full' },
  
  // Standard catalog listing route
  { path: 'games', component: GameListComponent },
  
  // Create game route using Reactive form
  { path: 'games/add', component: AddGameFormComponent },
  
  // Dynamic parameter route: matches paths like /games/1 or /games/abc
  { path: 'games/:id', component: GameDetailComponent },
  
  // Wildcard fallback route: matches any invalid URL and handles 404s
  { path: '**', redirectTo: 'games' }
];
