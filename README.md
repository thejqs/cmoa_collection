# Museums are a little weird.

But deeply fun to explore. As an excuse to try out a project involving [`pipenv`](https://docs.pipenv.org/) and [`Datasette`](https://github.com/simonw/datasette), I've decided to play around a bit with some of the collections data from the Carnegie Museum of Art.

CMOA helpfully makes a decent amount of [data public](https://github.com/cmoa/collection) about its collections. And while the museum doesn't update things on GitHub all that often, we have the added benefit(?) of the collection-search tools on their website being down at the moment. So we can explore some of the data even while the public can't.

![Like I said.](https://raw.githubusercontent.com/thejqs/cmoa_collection/master/search_down.png)

What's here so far is a small dataset that kind of amuses me: items with both unknown creators and anonymous donors. So often something is in a museum because of its provenance or its story. And here we largely have neither.

And we can learn a few things rather quickly:
* The vast majority of these items were donated on one day, December 6, 1979, with only two coming to CMOA after 1981
* Only five are listed as being on view, all in the 'Art Before 1300' Gallery
* Nearly half are Italian in origin
* All belong to the Decorative Arts and Design department
* Silk and velvet figure prominently as media in this dataset
* And sometimes, our anonymous donors have named co-donors: the Estate of John Henry Craner, Robert S. Waters Charitable Trust Fund, Women's Committee Fund

For now, know that with `pipenv` installed (`brew install pipenv`, perhaps?), an environment setup and then installing the dependencies in the lockfiles here, you're ready to clone down the CMOA repo to get at the collections `csv`. From there, you can use Pandas and a Jupyter notebook to explore the data yourself, or reproduce the `csv` here with `unknown_by_anonymous.py`.

After that, if you're so inclined, use the `unknowns_to_sqlite_loader.py` script to prepare the data to become a `Datasette` API.

Meantime, I'll keep hunting around my own self.
