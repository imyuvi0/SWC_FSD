import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

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
  private apiUrl = 'https://swc-fsd.vercel.app/api/games/';

  constructor(private http: HttpClient) {}

  private getHttpOptions() {
    // Read the authorization token from localStorage, fallback to pre-generated admin token for testing
    const token = localStorage.getItem('token') || '8bdecdaffb820e0d53abbbc8c8fe0ca69b3e8e88';
    return {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Token ${token}`
      })
    };
  }

  // Fetch games list from the live Django API
  getGames(): Observable<Game[]> {
    return this.http.get<Game[]>(this.apiUrl);
  }

  // Add a new game via a POST request to the Django API
  addGame(title: string, price: number): Observable<Game> {
    return this.http.post<Game>(this.apiUrl, { title, price }, this.getHttpOptions());
  }

  // Find a specific game by its numeric ID from the Django API
  getGameById(id: number): Observable<Game> {
    return this.http.get<Game>(`${this.apiUrl}${id}/`);
  }
}
