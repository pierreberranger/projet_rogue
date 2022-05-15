Pour lancer le jeu : aller dans le dossier projet_rogue_team_convolution.
Ensuite executer app.py en tapant python app.py dans un terminal.

## Connexions

Avec le navigateur, se connecter à localhost:5000/ pour jouer. Il est possbile de jouer en multijoueur comme expliqué directement dans la page d'accueil.   

Vous pouvez également jouer sur différents ordinateurs, en changeant le paramètre host de app.py et en y rentrant votre adresse ip. Attention il est possible que votre ordinateur possède un pare-feu et empêche les autres joueurs de se connecter à votre ordinateur depuis le même réseau, il faut alors le désactiver pour l'adresse ip de votre ami. Ce choix n'est pas recommandé pour des raisons évidentes de sécurité douteuse du code ;).
## Multijoueur
- Les monstres sont de niveau fixe: moyen, ils sont cachés et ne se révèlent que lorsque l'on passe à côté d'eux. On peut utiliser la barre espace pour tirer sur un ennemi (sur une case adjacente), que ce soit un monstre ou un joueur. Le tir ne réussit pas forcément, on peut trouver des armes pour augmenter ses chances de réussite au tir (symbôle ambulance).

- Pour rejoindre la même partie multijoueur que les autres, il suffit de rentrer un game id  (correspondant à une partie créée précédemment en appuyant sur le bouton "create a multiplayer game") et de clicker sur join a multiplayer game . Il n'y pas de limite de nombre de joueur. On ne peux pas jouer en multiplayer dans le même navigateur , car le player_id est stocké dans un cookie (ce qui suit la logique de l'implementation du jeu sur un serveur avec des joeurs connectés sur différents pc )

## Mode Solo
Le mode solo dispose de plusieurs niveaux, auxquels on peut accéder par des portails de téléportation, plus on monte dans les niveaux, plus les monstres sont forts.
### Sauvegarde
La sauvegarde de la partie en mode solo se fait directement sur la page de jeu. Il suffit de cliquer sur le bouton "come back later" puis lors d'une reconnection de cliquer sur start/resume a player game (si une partie est enregitrée, vous accéderez à celle-ci, sinon c'est une nouvelle partie qui vous sera proposée). Attention cette fonctionnalitée utilise des cookies, si vous arrêtez le serveur sans avoir pû cliquer sur discard the game, lorsque l'on relance le serveur le cookie est encore là mais la partie n'existe pas dans le nouveau serveur. Ce bug n'est pas censé apparaitre car le serveur n'a pas vocation à s'arrêter. Si toutefois vous rencontrez ce besoin, n'oubliez pas de supprimer manuellement les cookies avant de recommencer à jouer. 

## Contrôles

Pour ce qui est des contrôles : tous les joueurs ont les mêmes : les flèches et le pad du clavier servent à se déplacer, la barre espace à tirer, la touche enter à rejoindre la partie.


**Remarque:** Un membre du groupe (Pierre Berranger) n'a pas réussi à faire partie du git team-convolution (problèmes techniques), nous avons donc créé un autre git sur lequel nous avons travaillé : https://github.com/pierreberranger/projet_rogue vous pouvez vous y rendre pour voir l'historique git du jeu