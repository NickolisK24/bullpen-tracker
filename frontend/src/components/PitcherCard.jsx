// src/components/PitcherCard.jsx

// Enhanced team logo mapping with fallback (add more as needed)
const TEAM_LOGOS = {
  Mets: '/logos/mets.png',
  Phillies: '/logos/phillies.png',
  Angels: '/logos/angels.png',
  Dodgers: '/logos/dodgers.png',
  Yankees: '/logos/yankees.png',
  Braves: '/logos/braves.png',
  'D-backs': '/logos/dbacks.png',
  Giants: '/logos/giants.png',
  Padres: '/logos/padres.png',
  Astros: '/logos/astros.png',
  Guardians: '/logos/guardians.png',
  'White Sox': '/logos/whitesox.png',
  Brewers: '/logos/brewers.png',
  'Red Sox': '/logos/redsox.png'
}

const FALLBACK_LOGO = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'

export default function PitcherCard({ pitcher }) {
  const { name, handedness, fatigue, team } = pitcher

  const getFatigueColor = fatigue => {
    if (fatigue >= 90) return 'bg-red-500';
    if (fatigue >= 75) return 'bg-orange-400';
    if (fatigue >= 50) return 'bg-yellow-400';
    return 'bg-green-400';
  }

  // Try exact match, then fallback
  const logoUrl = TEAM_LOGOS[team] || FALLBACK_LOGO

  return (
    <div className="bg-white rounded-2xl p-6 shadow-lg border border-slate-200 hover:shadow-2xl hover:border-blue-400 transition duration-200 flex flex-col justify-between items-center text-center w-full min-h-80 mx-auto">
      {/* Logo far left, name top-middle, info below */}
      <div className="flex flex-row items-center w-full bg-white rounded-xl shadow-lg border border-slate-200 p-6 mb-6 hover:shadow-xl transition-all">
        {/* Logo */}
        <div className="flex items-center justify-center h-20 w-20 shrink-0 mr-6">
          <img
            src={TEAM_LOGOS[team] || FALLBACK_LOGO}
            alt={team + ' logo'}
            className="h-16 w-16 rounded-full object-cover border-2 border-blue-200 bg-white"
            onError={e => { e.target.onerror = null; e.target.src = FALLBACK_LOGO; }}
          />
        </div>
        {/* Info */}
        <div className="flex-1 flex flex-col gap-2">
          <h2 className="text-2xl font-bold text-blue-700 mb-1 text-left tracking-tight">{name}</h2>
          <div className="flex flex-row items-center gap-3 mb-2">
            <span className="text-xs px-2 py-1 rounded bg-blue-50 border border-blue-200 text-blue-700 font-mono">{handedness}</span>
            <span className="text-base text-slate-600 font-semibold">{team}</span>
          </div>
          {/* Fatigue Bar */}
          <div className="flex items-center gap-3 mt-2">
            <div className="w-40 bg-slate-100 h-5 rounded-full overflow-hidden border border-slate-200">
              <div
                className={`h-full transition-all duration-500 ${getFatigueColor(fatigue)}`}
                style={{ width: `${fatigue}%` }}
              />
            </div>
            <span className="text-lg font-mono px-2 py-1 rounded bg-slate-50 border border-slate-200">{fatigue}%</span>
          </div>
          {/* Alert */}
          {fatigue >= 90 && (
            <p className="text-sm mt-2 text-red-500 font-semibold flex items-center gap-1">
              <span className="text-xl">⚠️</span> High fatigue — consider rest
            </p>
          )}
        </div>
      </div>
      {/* Team Name */}
      <p className="text-sm text-slate-500 mb-2">{team}</p>
      {/* Fatigue Bar */}
      <div className="w-full bg-slate-200 h-4 rounded-full overflow-hidden mb-3">
        <div
          className={`h-full ${getFatigueColor(fatigue)} transition-all duration-500`}
          style={{ width: `${fatigue}%` }}
        />
      </div>
      <div className="flex items-center justify-center gap-2 mb-2">
        <span className="text-lg font-semibold">Fatigue:</span>
        <span className="text-lg font-mono px-2 py-1 rounded bg-slate-50 border border-slate-200">{fatigue}%</span>
      </div>
      {/* Alert */}
      {fatigue >= 90 && (
        <p className="text-sm mt-2 text-red-500 font-semibold flex items-center justify-center gap-1">
          <span className="text-xl">⚠️</span> High fatigue — consider rest
        </p>
      )}
    </div>
  )
}
