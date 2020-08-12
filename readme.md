<a href="http://onefootball.com/"><img src="https://lh3.googleusercontent.com/mXog2BuRhYPqKITgx29PpfjFoqAESP3PXF96dc0UEQPz4CxD35xL3cyfw-OECqA2baiR" width="125" height="125" align="right" /></a>

# onefootball_network

> Python client for the [OneFootball Network API](https://docs.network-api.onefootball.com/en/latest/api.html)

![PyPI](https://img.shields.io/pypi/v/onefootball-network?style=flat-square)
![Platform](https://img.shields.io/badge/python-3.7-blue.svg?style=flat-square)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square"></a>

This package contains a python client for the OneFootball Network API. It allows OneFootball’s content partners to publish articles onto the OneFootball platform. It also allows partners to update and delete articles that they have already published to the OneFootball platform.

The API can be used by partners to set up their own services such that content published on their sites is automatically sent to OneFootball and natively integrated onto the OneFootball platform for OneFootball users.

Please note that the OneFootball Network is a closed, invite-only platform and only authorized content partners are able to use the OneFootball Network API.

## 🚀 Quickstart

You can install `onefootball-network-api-py` from pip:

```sh
pip install onefootball-network-api-py
```

The package includes a `OneFootballNetwork` class which has all methods you need to interact with the api.

```python
# main.py
from onefootball_network import OneFootballNetwork, NewPost

of = OneFootballNetwork()

article = NewPost(
    external_id="28961",
    source_url="https://www.clermontfoot.com/amical-orleans-clermont-annule/",
    language="fr",
    published="2020-08-10T08:28:58Z",
    title="Amical : Orl\u00e9ans &#8211; Clermont annul\u00e9",
    content="""<p>A la demande de l&rsquo;US Orl\u00e9ans, le match amical du mercredi
        12 ao\u00fbt opposant l&rsquo;US Orl\u00e9ans et le Clermont Foot 63 \u00e0 Moulins,
        est annul\u00e9.</p> <p>Le prochain match amical du CF63 est pr\u00e9vu le
        samedi 15 ao\u00fbt contre Grenoble et sera retransmis sur le site de
        La Montagne dans le cadre de notre partenariat.</p>""",
)
post = of.publish_article(article)
print(post.onefootball_id)
```

## 🔧 Development

If you want to contribute to this repository, clone the git repository and run:

```sh
make develop
make test
make serve-docs
```

## Release History

- 0.1.0: first release

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
