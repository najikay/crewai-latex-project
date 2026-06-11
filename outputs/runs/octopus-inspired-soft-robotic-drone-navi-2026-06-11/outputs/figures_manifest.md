# Figures Manifest — Octopus-Inspired Soft Robotic Drone Navigation Using Bio-Mimetic SLAM

| # | Filename | Title | Hebrew Caption | LaTeX Label |
|---|----------|-------|----------------|-------------|
| 1 | `fig_octopus_biological_inspiration.png` | Biological inspiration from octopus nervous system to distributed SLAM architecture | איור 1: השראה ביולוגית ממערכת העצבים המבוזרת של התמנון לארכיטקטורת SLAM מבוזרת. (א) מערכת עצבים של תמנון עם מוח מרכזי ו-8 גנגליונים פריפריאליים. (ב) ארכיטקטורת SLAM מבוזרת עם צומת מרכזי ו-6 תתי-גרפים עצמאיים לכל זרוע. | \label{fig:octopus_biological_inspiration} |
| 2 | `fig_system_overview.png` | High-level system block diagram | איור 2: דיאגרמת מערכת כוללת של רחפן רך רב-זרועי לניווט תת-ימי. המערכת כוללת: רחפן רך, מערך חיישנים, מיזוג חיישנים רב-מודאלי, SLAM מבוזר, תכנון תנועה אדפטיבי, מיפוי סביבה היברידי, ולולאת משוב. | \label{fig:system_overview} |
| 3 | `fig_soft_arm_kinematics.png` | Kinematic model of multi-arm soft drone | איור 3: מודל קינמטי של רחפן רך רב-זרועי. (א) גאומטריית PCC (Piecewise Constant Curvature) לקטע זרוע רציפה בודד, עם פרמטרים: עקמומיות κ, זווית כיפוף φ, אורך קשת l, ורדיוס עקמומיות r. (ב) דגם תלת-ממדי של רחפן 6-זרועות עם מערכות צירים בכל קצה זרוע. | \label{fig:soft_arm_kinematics} |
| 4 | `fig_tactile_sensor_array.png` | Distributed tactile sensor array and curvature sensor calibration | איור 4: חישת מישוש מבוזרת בהשראת כפתורי היניקה של התמנון. (א) מערך חיישני מישוש על זרוע בודדת: 16 חיישנים קיבוליים, 4 חיישני עקמומיות (אפקט הול), וחיישן לחץ הידרוסטטי. (ב) עקומת כיול של חיישן עקמומיות מבוסס אפקט הול עם רגרסיה לינארית. | \label{fig:tactile_sensor_array} |
| 5 | `fig_sensor_fusion_architecture.png` | Multi-modal sensor fusion architecture with uncertainty propagation | איור 5: ארכיטקטורת מיזוג חיישנים רב-מודאלי. דיאגרמת בלוקים המציגה את זרימת הנתונים מ-5 סוגי חיישנים (סונאר, מצלמה סטריאו, חיישני מישוש, IMU+לחץ, GPS) דרך שלבי עיבוד מקדימים אל מרכז המיזוג (פילטר חלקיקים) ופלט: הערכת מצב, מפת סביבה, ואי-ודאות SLAM. | \label{fig:sensor_fusion_architecture} |
| 6 | `fig_distributed_factor_graph.png` | Distributed factor graph SLAM and ADMM consensus convergence | איור 6: SLAM מבוזר בהשראת מערכת העצבים של התמנון. (א) גרף פקטורים מבוזר עם 6 תתי-גרפים (זרועות), צומת מרכזי, ואילוצים בין-זרועיים. (ב) התכנסות אלגוריתם ADMM מבוזר עבור קצבי תקשורת שונים (10%, 50%, 100%) בהשוואה ל-SLAM ריכוזי. | \label{fig:distributed_factor_graph} |
| 7 | `fig_reinforcement_learning_architecture.png` | Multi-agent PPO architecture and example navigation trajectory | איור 7: תכנון תנועה אדפטיבי באמצעות למידת חיזוק מבוזרת. (א) ארכיטקטורת PPO רב-סוכן עם מבקר מרכזי (פונקציית ערך משותפת) ושחקנים מבוזרים (פוליסות עצמאיות לכל זרוע). (ב) מסלול ניווט לדוגמה בסביבה תת-ימית עם מכשולים, אליפסות אי-ודאות, ונקודות התחלה ויעד. | \label{fig:reinforcement_learning_architecture} |
| 8 | `fig_occupancy_grid_comparison.png` | Occupancy grid comparison: sonar-only, tactile-only, and hybrid | איור 8: השוואת מפות תפוסה בסביבה תת-ימית מובנית. (א) מפת אמת. (ב) מיפוי סונאר בלבד. (ג) מיפוי מישוש בלבד. (ד) מיפוי היברידי (סונאר+מישוש). (ה-ו) מפות שגיאה למיפוי סונאר ומישוש בהתאמה. המיפוי ההיברידי מפיק את התוצאות המדויקות ביותר. | \label{fig:occupancy_grid_comparison} |
| 9 | `fig_trajectory_comparison.png` | Trajectory comparison and error metrics (ATE/RPE) | איור 9: תוצאות סימולציה - השוואת ביצועי מערכת הניווט הביומימטית. (א) מסלולים תלת-ממדיים במערה תת-ימית: מסלול אמת, SLAM ריכוזי, SLAM מבוזר (מוצע), ו-ORB-SLAM3 תת-ימי. (ב) תיבות-שפם של ATE ו-RPE עבור 4 שיטות שונות על פני 50 הרצות מונטה-קרלו. השיטה המוצעת (SLAM מבוזר+מישוש) משיגה שיפור של 44% ב-ATE. | \label{fig:trajectory_comparison} |

---

**Total: 9 figures generated**
- Format: PNG, 300 DPI
- Style: seaborn-v0_8-whitegrid
- Minimum font size: 11pt
- All figures include: descriptive titles, labeled axes with units, legends (where applicable), Hebrew captions