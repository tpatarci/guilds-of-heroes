import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <div className="not-found">
      <h1 className="not-found__title">YOU DIED</h1>
      <p className="not-found__message">
        The page you seek has fallen<br />
        into the dungeon abyss.<br />
        Error 404 — Page Not Found
      </p>
      <div className="not-found__skull">
        <span role="img" aria-label="skull">&#x1F480;</span>
      </div>
      <Link to="/" className="not-found__link">
        &#x2190; RESPAWN AT TAVERN
      </Link>
    </div>
  );
}
