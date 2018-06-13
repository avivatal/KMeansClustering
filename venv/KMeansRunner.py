from sklearn.cluster import KMeans
from PIL import Image
import matplotlib.pyplot as mat
import plotly.plotly as py


class KMeansRunner:

    def __init__(self, df, numberOfClusters, numberOfRuns):
        self.df=df
        self.numberOfClusters = numberOfClusters
        self.numberOfRuns = numberOfRuns

        # run kmeans algorithm
        kmeansRes = KMeans(n_clusters=numberOfClusters, n_init=numberOfRuns).fit(self.df)

        # update df
        pred = kmeansRes.predict(self.df)
        self.df['ClusterNumber'] = pred

        self.scatter()
        self.horopleth()

    def scatter(self):
        #scatter: x=social support, y=generosity, color by kmeans result
        self.scatter = mat.scatter(x=self.df['Social support'], y=self.df['Generosity'], c=self.df['ClusterNumber'])
        mat.colorbar(self.scatter)
        mat.xlabel("Social support")
        mat.ylabel("Generosity")
        mat.title("K-Means Clustering")
        mat.savefig('scatter.png')

    def horopleth(self):
        scl = [[0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'], [0.4, 'rgb(188,189,220)'],
               [0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'], [1.0, 'rgb(84,39,143)']]

        data = [dict(
            type='choropleth',
            colorscale=scl,
            autocolorscale=False,
            locations=self.df.axes[0].tolist(),
            z=self.df['ClusterNumber'],
            locationmode='country names',
            text=self.df.axes[0].tolist(),
            marker=dict(
                line=dict(
                    color='rgb(255,255,255)',
                    width=2
                )
            ),
            colorbar=dict(
                title="Cluster"
            )
        )]

        layout = dict(
            title='K-Means Clustering Visualization',
            geo=dict(
                scope='Cluster Group',
                projection=dict(type='Mercator'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)',
            ),
        )
        py.sign_in("talshemt", "zgAzXUHXrBOenhAwSiDz")
        fig = dict(data=data, layout=layout)
        py.plot(fig, validate=False, filename='d3-horopleth-map', auto_open=False)
        py.image.save_as(fig, filename='horopleth.png')
