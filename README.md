# 🎮 FIRING THE ENEMY

An intense action-packed shooter game built with Python and Pygame!

## 🎯 Game Features

- **80 Levels** with increasing difficulty
- **4 Unique Weapons**:
  - 🔫 **Pistol**: Fast firing, moderate damage
  - 🏹 **Rifle**: Spread shots, balanced stats
  - 🔱 **Shotgun**: Wide spread, close-range devastation
  - 🎯 **Sniper**: High damage, slow fire rate

- **3 Enemy Types**:
  - 🔴 **Basic**: Standard enemies
  - 💜 **Fast**: Quick and agile
  - 🟠 **Tanky**: Slow but durable

- **Dynamic Gameplay**:
  - Progressive difficulty scaling
  - Smart enemy AI
  - Real-time health tracking
  - Score and enemy kill counter
  - Ammo management system

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/zainali7862/zain.git
cd zain
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

## 🎮 How to Play

### Controls
- **Arrow Keys** or **WASD**: Move your character
- **Mouse Click**: Shoot in the direction of your cursor
- **Keys 1-4**: Switch weapons
  - **1**: Pistol
  - **2**: Rifle
  - **3**: Shotgun
  - **4**: Sniper

### Objective
- Survive and defeat all enemies in each wave
- Progress through 80 levels
- Achieve the highest score possible
- Manage your ammo and health wisely

### Weapons

#### Pistol (1)
- Damage: 10
- Fire Rate: Fast (10ms cooldown)
- Ammo: 30
- Speed: 7 pixels/frame
- Single shot, straightforward

#### Rifle (2)
- Damage: 20
- Fire Rate: Medium (5ms cooldown)
- Ammo: 60
- Speed: 8 pixels/frame
- Fires 3 bullets in a tight spread

#### Shotgun (3)
- Damage: 15 per pellet
- Fire Rate: Slow (20ms cooldown)
- Ammo: 24
- Speed: 6 pixels/frame
- Fires 8 pellets in a wide spread

#### Sniper (4)
- Damage: 50
- Fire Rate: Very Slow (40ms cooldown)
- Ammo: 12
- Speed: 10 pixels/frame
- Single powerful shot

## 📊 Progression

- Levels 1-20: Gentle introduction, mostly basic enemies
- Levels 21-50: Increased difficulty, more variety
- Levels 51-80: Extreme challenge, wave intensity increases

## 🎨 Graphics

- Player: Blue square
- Basic Enemy: Red square
- Fast Enemy: Purple square
- Tanky Enemy: Orange square
- Bullets: Color-coded by weapon
- Health bars for enemies

## 📈 Scoring

- Base points: 100 per enemy
- Level bonus: +10 per enemy per level
- Example: Level 50 = 600 points per enemy killed

## 💾 Game Features Implemented

✅ 80-level progression system
✅ 4 unique weapons with distinct mechanics
✅ Smart enemy AI with 3 types
✅ Dynamic difficulty scaling
✅ Real-time scoring system
✅ Health management
✅ Ammo system
✅ Wave-based enemy spawning
✅ Smooth collision detection
✅ Game over and victory screens

## 🔧 Technical Details

- **Engine**: Pygame
- **Language**: Python 3.8+
- **Resolution**: 1200x800 pixels
- **FPS**: 60
- **Architecture**: Object-oriented with sprite-based gameplay

## 🎓 Code Structure

- `WeaponType`: Enum for weapon types
- `Weapon`: Dataclass for weapon properties
- `Player`: Main player character class
- `Bullet`: Projectile class
- `Enemy`: Enemy character with AI
- `Game`: Main game loop and logic

## 🐛 Known Limitations

- No persistent save system
- No sound effects (can be added)
- No multiplayer
- Graphics are simple geometric shapes

## 📝 Future Enhancements

- [ ] Sound effects and music
- [ ] Power-ups and special items
- [ ] Boss battles
- [ ] Leaderboard system
- [ ] Particle effects
- [ ] Better graphics/sprites
- [ ] Weapon upgrades
- [ ] Different game modes

## 📄 License

MIT License - Feel free to use and modify!

## 👨‍💻 Author

Created with ❤️ by Zain Ali

---

**Good luck, soldier! The enemy awaits! 🎯🔫**
