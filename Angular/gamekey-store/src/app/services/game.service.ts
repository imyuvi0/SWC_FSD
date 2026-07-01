import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

export interface Game {
  id: number;
  title: string;
  price: number;
  available: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class GameService {
  private games: Game[] = [
    { id: 1, title: 'Half-Life 3', price: 29.99, available: true },
    { id: 2, title: 'Cyberpunk 2077', price: 49.99, available: false },
    { id: 3, title: 'Portal 3', price: 19.99, available: true }
  ];

  constructor() {}

  // Fetch games list as an Observable stream
  getGames(): Observable<Game[]> {
    return of(this.games);
  }

  // Append a new game to the local inventory list
  addGame(title: string, price: number): Observable<Game> {
    const newGame: Game = {
      id: this.games.length + 1,
      title: title,
      price: price,
      available: true
    };
    this.games.push(newGame);
    return of(newGame);
  }

  // Find a specific game by its numeric ID
  getGameById(id: number): Observable<Game | undefined> {
    const game = this.games.find(g => g.id === id);
    return of(game);
  }
}
