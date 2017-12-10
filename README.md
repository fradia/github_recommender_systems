# Recommender systems for GitHub Users

In this project different techniques to build a recommender system for GitHub users are presented. 
The main goal is to provide users with information about repositories they might find interesting. The approach used is based on collaborative filtering:
the historical users interactions with repositories are considered to "understand" users preferences. In particular the focus of the project is on forks and stars.

Currently GitHub provides an [explore page]("https://github.com/explore") page 
with articles regarding popular projects and other GitHub events.

In the [GHRecommender]("href="https://ghrecommender.io/") a recommender system is built using collaborative filtering based on stars.
In this project a similar approach is chosen but with two sets of interactions of users with repositories: stars and forks. Moreover, different models are tested: explicit and implicit collaborative
filtering and the universal recommender.


## Data

Github provides data about public event through a [REST API](https://developer.github.com/). The data considered in this project come from
the [GHTorrent database]("http://ghtorrent.org/") stored in [Google Cloud platform]("https://cloud.google.com/?hl=en"). The database contains 4TB of data
and for practical reasons only a sample of data is considered here. 
One of the big challenge of this project is to deal with users that are very active. As the distribution of stars and forks by users show most of the users starred and forked very few repositories.
Also some outliers (users with 7000 stars) have to be considered.

:-:|:-:|:-:
![](github_recommender_systems/ALS/dist_forks_log.png) | ![](github_recommender_systems/ALS/dist_stars_log.png ) 

For these reasons only users that have forked at least 20 repos or starred at least 5 repos are considered. Outliers are also removed.


## Models

### Collaborative Filtering

In the collaborative filtering approach a user-item association matrix is considered. In this case the items are GitHub repositories and the entries of the 
matrix represent a fork or a star
of a user to an item. The alternating least squares (ALS) algorithm is used to fill the missing values and give a 

#### ALS (explicit and implicit feedback)

ALS for explicit feedback is implemented using pyspark. The dataset is divided into train and test and the model is fitted on the train set. 

* Considering only forks as interaction of users with repositories and by taking parameters rank=20, maxIter=20 and regPar=0.1 a root mean squared 
error of 0.10 on the train set and of 0.19 on the test set are obtained.

* Considering forks and stars as interactions of users with repositories and by taking parameters rank=10, maxIter=10 and regPar=0.1 a root mean squared 
error of 0.09 on the train set and of 0.14 on the test set are obtained.

* Forks and stars are also considered in ALS for implicit feedback (with a rating of 1 and 0.7 respectively). In this case a much higher error on the . 
See [here](http://yifanhu.net/PUB/cf.pdf) for more information about collaborative filtering with implicit feedback.


#### Universal Recommender (UR)

The universal recommender is a type of collaborative filtering model where the recommendations are given based on co-occurrences between users interactions with items.
For more information on the idea behind the universal recommender see [here](http://actionml.com/docs/ur). 
In this project the universal recommender is deployed twice: once using forks as main and unique event and once using forks as main event and stars as secondary event.
A sample of the data used for ALS is considered. The data is divided into train and test set and the evaluation made is based on recall 
(% of items in the test set that are actually recommended by the models).

* Using forks as unique main event a recall of 58% is obtained
* Using forks as main event and stars as secondary event the recall improves to 60%

As the results show adding stars as secondary actions does not give a big advantage. Indeed the co-occurrence matrix between forks and stars is quite sparse
and does not give much additional information on the users preferences. Indeed in the sample data considered only 10% of the users who forked repositories 
also starred repositories. 
Moreover forks and stars are in general not very co-occurrent (not so many users fork a set of repositories AND star a set of other repositories). 
One possible solution would be to sample the data in a different way but enlarging the dataset can cause even more sparsity.


#### Models comparison

There is no starighforward way to compare the models (ALS and UR). The approach used here is to take at the items in the test sets
that were recommended by the models and look at the distributions of the normalized recommendations scores on those items.

Figure1 Figure2


It seems ALS is performing better (the items that are in the test set are given a higher score by the recommender) but it is difficult to make a clear comparison.

### Implementation of UR

The universal recommender is based on Prediction IO. Clone the repository [here](https://github.com/actionml/universal-recommender) to test it.
For the installation of Prediction IO follow [these instructions](http://actionml.com/docs/install).
For this project a docker container containing Preidiction IO+Universal Recommender was used. See [here](https://github.com/gozutok/docker-universalrecommender) to create
the docker container.

After cloning the universal recommender repository in a folder run

```
docker run -v path_to_your_folder:/root -it --rm -p 8000:8000 -p 7070:7070 gozutok/universalrecommender /bin/bash
```

To start pio run

```
pio-start-all
```

Follow [these instructions](http://actionml.com/docs/ur_quickstart) to run an integration test. Similarly to the integration test you can run the files 
```
./pio_forks.sh
```

and

```
./pio_forks_stars.sh
```

Make sure all the files contained in ... are copied in your own folder.

To retrieve recommendation open a new tab and run

```
./pio_exports_forks_stars.sh
```

### Folder description

* ALS contains all the notebooks for ALS implementation. The data folder contains the sql queries used to retrieve the data from GHTorrent database
* UR contains all the notebooks, engines and shell scripts for UR implementations. The notebook ur_data_preparation.ipynb describes how
the data is selected. The data folder contains samples for two users for illustrative purpose.
* RECOMMEND contains a notebook to retrieve recommendations from the two models and save them in a SQLite database. It also contains a Flask application to retrieve the
recommendations. The backend and frontend of the application were made with the help of [Jesus Martinez Blanco](https://github.com/chumo).





