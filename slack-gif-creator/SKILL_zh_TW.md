---
name: slack-gif-creator
description: 用於建立針對 Slack 優化的動態 GIF 之工具包，具備大小限制驗證器與可組合的動畫基本單元。當使用者要求根據描述（如「製作一個 X 正在做 Y 的 Slack GIF」）製作動態 GIF 或表情符號動畫時適用。
license: 完整條款請參閱 LICENSE.txt
---

# Slack GIF 創作工具 - 靈活工具包 (Slack GIF Creator)

這是一個用於建立針對 Slack 優化的動態 GIF 工具包。提供符合 Slack 限制條件的驗證器、可組合的動畫基本單元以及選配的輔助公用程式。**請根據創意需求靈活運用這些工具。**

## Slack 的要求

Slack 對不同用途的 GIF 有特定要求：

**訊息用 GIF (Message GIFs):**
- 最大檔案大小：約 2MB
- 最佳尺寸：480x480
- 典型幀率 (FPS)：15-20
- 顏色限制：128-256 色
- 時長：2-5 秒

**表情符號用 GIF (Emoji GIFs):**
- 最大檔案大小：64KB (嚴格限制)
- 最佳尺寸：128x128
- 典型幀率 (FPS)：10-12
- 顏色限制：32-48 色
- 時長：1-2 秒

**製作表情符號用 GIF 具備挑戰性** —— 64KB 的限制非常嚴格。有助於達標的策略：
- 總幀數限制在 10-15 幀內。
- 最多使用 32-48 種顏色。
- 保持設計簡潔。
- 避免使用漸層。
- 頻繁驗證檔案大小。

## 工具包結構

此技能提供三種類型的工具：

1. **驗證器 (Validators)** —— 檢查 GIF 是否符合 Slack 的要求。
2. **動畫基本單元 (Animation Primitives)** —— 可組合的運動組件（抖動、彈跳、移動、萬花筒）。
3. **輔助公用程式 (Helper Utilities)** —— 用於常見需求（文字、顏色、特效）的選配函式。

**在如何應用這些工具方面，您具備完全的創作自由。**

## 核心驗證器

為了確保 GIF 符合 Slack 的約束條件，請使用以下驗證器：

```python
from core.gif_builder import GIFBuilder

# 建立 GIF 後，檢查是否符合要求
builder = GIFBuilder(width=128, height=128, fps=10)
# ... 按您的需求新增幀 (Frames) ...

# 儲存並檢查大小
info = builder.save('emoji.gif', num_colors=48, optimize_for_emoji=True)

# save 方法會在檔案超出限制時自動發出警告
# info 字典包含：size_kb, size_mb, frame_count, duration_seconds
```

**檔案大小驗證器**:
```python
from core.validators import check_slack_size

# 檢查 GIF 是否符合大小限制
passes, info = check_slack_size('emoji.gif', is_emoji=True)
# 回傳：(True/False, 包含大小詳情的字典)
```

**尺寸驗證器**:
```python
from core.validators import validate_dimensions

# 檢查尺寸
passes, info = validate_dimensions(128, 128, is_emoji=True)
# 回傳：(True/False, 包含尺寸詳情的字典)
```

**完整驗證**:
```python
from core.validators import validate_gif, is_slack_ready

# 執行所有驗證
all_pass, results = validate_gif('emoji.gif', is_emoji=True)

# 或快速檢查
if is_slack_ready('emoji.gif', is_emoji=True):
    print("準備好上傳了！")
```

## 動畫基本單元 (Animation Primitives)

這些是可組合的運動組件。可以將其應用於任何物件的任何組合：

### 抖動 (Shake)
```python
from templates.shake import create_shake_animation

# 讓表情符號抖動
frames = create_shake_animation(
    object_type='emoji',
    object_data={'emoji': '😱', 'size': 80},
    num_frames=20,
    shake_intensity=15,
    direction='both'  # 或 'horizontal', 'vertical'
)
```

### 彈跳 (Bounce)
```python
from templates.bounce import create_bounce_animation

# 讓圓形彈跳
frames = create_bounce_animation(
    object_type='circle',
    object_data={'radius': 40, 'color': (255, 100, 100)},
    num_frames=30,
    bounce_height=150
)
```

### 旋轉 (Spin / Rotate)
```python
from templates.spin import create_spin_animation, create_loading_spinner

# 順時針旋轉
frames = create_spin_animation(
    object_type='emoji',
    object_data={'emoji': '🔄', 'size': 100},
    rotation_type='clockwise',
    full_rotations=2
)

# 擺動旋轉 (Wobble)
frames = create_spin_animation(rotation_type='wobble', full_rotations=3)

# 載入中轉圈 (Loading spinner)
frames = create_loading_spinner(spinner_type='dots')
```

### 脈動 / 心跳 (Pulse / Heartbeat)
```python
from templates.pulse import create_pulse_animation, create_attention_pulse

# 平滑脈動
frames = create_pulse_animation(
    object_data={'emoji': '❤️', 'size': 100},
    pulse_type='smooth',
    scale_range=(0.8, 1.2)
)

# 心跳 (雙重跳動)
frames = create_pulse_animation(pulse_type='heartbeat')

# 用於表情符號 GIF 的注意脈動
frames = create_attention_pulse(emoji='⚠️', num_frames=20)
```

### 漸變 (Fade)
```python
from templates.fade import create_fade_animation, create_crossfade

# 漸入
frames = create_fade_animation(fade_type='in')

# 漸出
frames = create_fade_animation(fade_type='out')

# 兩個表情符號之間的交錯漸變 (Crossfade)
frames = create_crossfade(
    object1_data={'emoji': '😊', 'size': 100},
    object2_data={'emoji': '😂', 'size': 100}
)
```

### 縮放 (Zoom)
```python
from templates.zoom import create_zoom_animation, create_explosion_zoom

# 戲劇性放大
frames = create_zoom_animation(
    zoom_type='in',
    scale_range=(0.1, 2.0),
    add_motion_blur=True
)

# 縮小
frames = create_zoom_animation(zoom_type='out')

# 爆炸式縮放
frames = create_explosion_zoom(emoji='💥')
```

### 爆炸 / 碎裂 (Explode / Shatter)
```python
from templates.explode import create_explode_animation, create_particle_burst

# 噴發式爆炸
frames = create_explode_animation(
    explode_type='burst',
    num_pieces=25
)

# 碎裂效果
frames = create_explode_animation(explode_type='shatter')

# 溶解成粒子
frames = create_explode_animation(explode_type='dissolve')

# 粒子噴發
frames = create_particle_burst(particle_count=30)
```

### 扭動 / 擺動 (Wiggle / Jiggle)
```python
from templates.wiggle import create_wiggle_animation, create_excited_wiggle

# 果凍式擺動 (Jello wobble)
frames = create_wiggle_animation(
    wiggle_type='jello',
    intensity=1.0,
    cycles=2
)

# 波浪運動
frames = create_wiggle_animation(wiggle_type='wave')

# 用於表情符號 GIF 的興奮扭動
frames = create_excited_wiggle(emoji='🎉')
```

### 滑動 (Slide)
```python
from templates.slide import create_slide_animation, create_multi_slide

# 從左側滑入並帶有衝過頭 (Overshoot) 效果
frames = create_slide_animation(
    direction='left',
    slide_type='in',
    overshoot=True
)

# 滑過畫面
frames = create_slide_animation(direction='left', slide_type='across')

# 多個物件依序滑動
objects = [
    {'data': {'emoji': '🎯', 'size': 60}, 'direction': 'left', 'final_pos': (120, 240)},
    {'data': {'emoji': '🎪', 'size': 60}, 'direction': 'right', 'final_pos': (240, 240)}
]
frames = create_multi_slide(objects, stagger_delay=5)
```

### 翻轉 (Flip)
```python
from templates.flip import create_flip_animation, create_quick_flip

# 兩個表情符號之間的水平翻轉
frames = create_flip_animation(
    object1_data={'emoji': '😊', 'size': 120},
    object2_data={'emoji': '😂', 'size': 120},
    flip_axis='horizontal'
)

# 垂直翻轉
frames = create_flip_animation(flip_axis='vertical')

# 用於表情符號 GIF 的快速翻轉
frames = create_quick_flip('👍', '👎')
```

### 變形 (Morph / Transform)
```python
from templates.morph import create_morph_animation, create_reaction_morph

# 交錯漸變變形
frames = create_morph_animation(
    object1_data={'emoji': '😊', 'size': 100},
    object2_data={'emoji': '😂', 'size': 100},
    morph_type='crossfade'
)

# 縮放變形（一個縮小，另一個長大）
frames = create_morph_animation(morph_type='scale')

# 旋轉變形（類似 3D 翻轉）
frames = create_morph_animation(morph_type='spin_morph')
```

### 移動效果 (Move Effect)
```python
from templates.move import create_move_animation

# 線性移動
frames = create_move_animation(
    object_type='emoji',
    object_data={'emoji': '🚀', 'size': 60},
    start_pos=(50, 240),
    end_pos=(430, 240),
    motion_type='linear',
    easing='ease_out'
)

# 弧形移動（拋物線軌跡）
frames = create_move_animation(
    object_type='emoji',
    object_data={'emoji': '⚽', 'size': 60},
    start_pos=(50, 350),
    end_pos=(430, 350),
    motion_type='arc',
    motion_params={'arc_height': 150}
)

# 圓形移動
frames = create_move_animation(
    object_type='emoji',
    object_data={'emoji': '🌍', 'size': 50},
    motion_type='circle',
    motion_params={
        'center': (240, 240),
        'radius': 120,
        'angle_range': 360  # 完整一圈
    }
)

# 波浪移動
frames = create_move_animation(
    motion_type='wave',
    motion_params={
        'wave_amplitude': 50,
        'wave_frequency': 2
    }
)

# 或使用底層的緩動 (Easing) 函式
from core.easing import interpolate, calculate_arc_motion

for i in range(num_frames):
    t = i / (num_frames - 1)
    x = interpolate(start_x, end_x, t, easing='ease_out')
    # 或：x, y = calculate_arc_motion(start, end, height, t)
```

### 萬花筒效果 (Kaleidoscope Effect)
```python
from templates.kaleidoscope import apply_kaleidoscope, create_kaleidoscope_animation

# 套用於單一幀
kaleido_frame = apply_kaleidoscope(frame, segments=8)

# 或建立萬花筒動畫
frames = create_kaleidoscope_animation(
    base_frame=my_frame,  # 或為 None 使用示範模式
    num_frames=30,
    segments=8,
    rotation_speed=1.0
)

# 簡單鏡像效果（速度更快）
from templates.kaleidoscope import apply_simple_mirror

mirrored = apply_simple_mirror(frame, mode='quad')  # 四向鏡像
# 模式：'horizontal', 'vertical', 'quad', 'radial'
```

**若要自由組合基本單元，請參考以下模式：**
```python
# 範例：彈跳 + 抖動以增加衝擊感
for i in range(num_frames):
    frame = create_blank_frame(480, 480, bg_color)

    # 彈跳運動
    t_bounce = i / (num_frames - 1)
    y = interpolate(start_y, ground_y, t_bounce, 'bounce_out')

    # 落地時增加抖動（當 y 到達地面時）
    if y >= ground_y - 5:
        shake_x = math.sin(i * 2) * 10
        x = center_x + shake_x
    else:
        x = center_x

    draw_emoji(frame, '⚽', (x, y), size=60)
    builder.add_frame(frame)
```

## 輔助公用程式 (Helper Utilities)

這些是用於常見需求的選配助手。**請根據需要使用、修改或替換為自訂實作。**

### GIF 生成器 (組裝與優化)

```python
from core.gif_builder import GIFBuilder

# 使用您選擇的設定建立生成器
builder = GIFBuilder(width=480, height=480, fps=20)

# 新增幀（無論您是如何建立它們的）
for frame in my_frames:
    builder.add_frame(frame)

# 儲存並進行優化
builder.save('output.gif',
             num_colors=128,
             optimize_for_emoji=False)
```

關鍵功能：
- 自動色彩量化 (Color quantization)。
- 重複幀移除。
- Slack 限制大小警告。
- 表情符號模式（激進優化）。

### 文字渲染 (Text Rendering)

對於表情符號等小型 GIF，文字可讀性是一項挑戰。常見的解決方案是新增描邊：

```python
from core.typography import draw_text_with_outline, TYPOGRAPHY_SCALE

# 帶描邊的文字（助於提升可讀性）
draw_text_with_outline(
    frame, "BONK!",
    position=(240, 100),
    font_size=TYPOGRAPHY_SCALE['h1'],  # 60px
    text_color=(255, 68, 68),
    outline_color=(0, 0, 0),
    outline_width=4,
    centered=True
)
```

若要實作自訂文字渲染，使用 PIL 的 `ImageDraw.text()` 對於較大的 GIF 效果良好。

### 色彩管理

專業感的 GIF 通常使用協調的調色盤：

```python
from core.color_palettes import get_palette

# 獲取預設調色盤
palette = get_palette('vibrant')  # 或 'pastel', 'dark', 'neon', 'professional'

bg_color = palette['background']
text_color = palette['primary']
accent_color = palette['accent']
```

若要直接處理顏色，使用 RGB 元組 (Tuples) 即可。

### 視覺特效

用於衝擊時刻的選配特效：

```python
from core.visual_effects import ParticleSystem, create_impact_flash, create_shockwave_rings

# 粒子系統
particles = ParticleSystem()
particles.emit_sparkles(x=240, y=200, count=15)
particles.emit_confetti(x=240, y=200, count=20)

# 更新並渲染每一幀
particles.update()
particles.render(frame)

# 閃光效果
frame = create_impact_flash(frame, position=(240, 200), radius=100)

# 衝擊波圓環
frame = create_shockwave_rings(frame, position=(240, 200), radii=[30, 60, 90])
```

### 緩動函式 (Easing Functions)

平滑的運動使用緩動而非線性插值：

```python
from core.easing import interpolate

# 物件下落（加速）
y = interpolate(start=0, end=400, t=progress, easing='ease_in')

# 物件著陸（減速）
y = interpolate(start=0, end=400, t=progress, easing='ease_out')

# 彈跳
y = interpolate(start=0, end=400, t=progress, easing='bounce_out')

# 衝過頭（具彈性）
scale = interpolate(start=0.5, end=1.0, t=progress, easing='elastic_out')
```

可用緩動：`linear`, `ease_in`, `ease_out`, `ease_in_out`, `bounce_out`, `elastic_out`, `back_out` (衝過頭) 等，詳見 `core/easing.py`。

### 幀合成 (Frame Composition)

如果您需要的基礎繪圖工具：

```python
from core.frame_composer import (
    create_gradient_background,  # 漸層背景
    draw_emoji_enhanced,         # 帶選配陰影的表情符號
    draw_circle_with_shadow,     # 具深度感的形狀
    draw_star                    # 五角星
)

# 漸層背景
frame = create_gradient_background(480, 480, top_color, bottom_color)

# 帶陰影的表情符號
draw_emoji_enhanced(frame, '🎉', position=(200, 200), size=80, shadow=True)
```

## 優化策略

當您的 GIF 檔案太大時：

**針對訊息用 GIF (>2MB)：**
1. 減少幀數（降低 FPS 或縮短時長）。
2. 減少顏色（128 → 64 色）。
3. 縮小尺寸（480x480 → 320x320）。
4. 啟用重複幀移除功能。

**針對表情符號用 GIF (>64KB) —— 需採取激進策略：**
1. 總幀數限制在 10-12 幀。
2. 最多使用 32-40 色。
3. 避免使用漸層（純色壓縮效果更好）。
4. 簡化設計（減少元素數量）。
5. 在 save 方法中使用 `optimize_for_emoji=True`。

## 範例合成模式

### 簡單反應（脈動）
```python
builder = GIFBuilder(128, 128, 10)

for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))

    # 脈動縮放
    scale = 1.0 + math.sin(i * 0.5) * 0.15
    size = int(60 * scale)

    draw_emoji_enhanced(frame, '😱', position=(64-size//2, 64-size//2),
                       size=size, shadow=False)
    builder.add_frame(frame)

builder.save('reaction.gif', num_colors=40, optimize_for_emoji=True)

# 驗證
from core.validators import check_slack_size
check_slack_size('reaction.gif', is_emoji=True)
```

### 具衝擊感的動作（彈跳 + 閃光）
```python
builder = GIFBuilder(480, 480, 20)

# 第一階段：物件落下
for i in range(15):
    frame = create_gradient_background(480, 480, (240, 248, 255), (200, 230, 255))
    t = i / 14
    y = interpolate(0, 350, t, 'ease_in')
    draw_emoji_enhanced(frame, '⚽', position=(220, int(y)), size=80)
    builder.add_frame(frame)

# 第二階段：落地衝擊 + 閃光
for i in range(8):
    frame = create_gradient_background(480, 480, (240, 248, 255), (200, 230, 255))

    # 前三幀顯示閃光
    if i < 3:
        frame = create_impact_flash(frame, (240, 350), radius=120, intensity=0.6)

    draw_emoji_enhanced(frame, '⚽', position=(220, 350), size=80)

    # 文字出現
    if i > 2:
        draw_text_with_outline(frame, "GOAL!", position=(240, 150),
                              font_size=60, text_color=(255, 68, 68),
                              outline_color=(0, 0, 0), outline_width=4, centered=True)

    builder.add_frame(frame)

builder.save('goal.gif', num_colors=128)
```

### 組合基本單元（移動 + 抖動）
```python
from templates.shake import create_shake_animation

# 建立抖動動畫
shake_frames = create_shake_animation(
    object_type='emoji',
    object_data={'emoji': '😰', 'size': 70},
    num_frames=20,
    shake_intensity=12
)

# 建立觸發抖動的移動元素
builder = GIFBuilder(480, 480, 20)
for i in range(40):
    t = i / 39

    if i < 20:
        # 觸發前 —— 使用帶有移動物件的空白幀
        frame = create_blank_frame(480, 480, (255, 255, 255))
        x = interpolate(50, 300, t * 2, 'linear')
        draw_emoji_enhanced(frame, '🚗', position=(int(x), 300), size=60)
        draw_emoji_enhanced(frame, '😰', position=(350, 200), size=70)
    else:
        # 觸發後 —— 使用抖動幀
        frame = shake_frames[i - 20]
        # 在最終位置加入汽車
        draw_emoji_enhanced(frame, '🚗', position=(300, 300), size=60)

    builder.add_frame(frame)

builder.save('scare.gif')
```

## 創作哲學

此工具包提供的是組件，而非死板的配方。處理 GIF 請求時：

1. **理解創意願景** —— 應該發生什麼事？氛圍如何？
2. **設計動畫** —— 拆分為不同階段（預期動作、主要動作、後續反應）。
3. **根據需要應用基本單元** —— 抖動、彈跳、移動、特效 —— 自由組合。
4. **驗證約束條件** —— 檢查檔案大小，特別是針對表情符號用 GIF。
5. **必要時進行迭代** —— 如果超出大小限制，則減少幀數或顏色。

**目標是在 Slack 的技術限制內實現最大的創作自由。**

## 依賴項

若要使用此工具包，請在尚未安裝時安裝以下依賴項：

```bash
pip install pillow imageio numpy
```
