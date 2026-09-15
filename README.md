# TP

Une transaction est invalide si une colonne est manquante, si le montant ne peut pas être converti en nombre, ou si la date est non conforme. Dans ce cas, la transaction est rejetée et on la compte, et on continue à travailler avec les autres transactions valides. Ce choix a été fait parce que je ne veux pas faire échouer tout le traitement à cause de quelques transactions non valides.
