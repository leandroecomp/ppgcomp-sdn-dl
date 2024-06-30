# SDN-DL
<div align="justify"> Classifying network traffic plays an important role in identifying which applications are being used by users on a data network. As a result, increasingly improved techniques are needed to identify increasingly diversified traffic. Classical approaches such as port identification or packet inspection are widely used to classify and analyze network traffic flows. However, in recent years, there has been an exponential growth in Internet traffic, due to the large increase in the number of users and the diversity of services. Technologies arising from Industry 4.0 such as IoT (Internet of Things), Blockchain and Big Data, have become very popular in recent years, and have encouraged investment in Software Defined Networks (SDN) architectures, which make the integration and convergence of these emerging technological concepts more flexible. Despite the benefits, the adoption of SDN brings new challenges, mainly in the field of cybersecurity, since new elements are inserted in the network. On the other hand, integration with IoT services, countless types of new devices and services, pose risks to security and network infrastructure. In recent years, we have witnessed the rise of Machine Learning in scientific research, with the considered most promising technique being the textit{Deep Learning}, which uses artificial neural networks of different architectures to the most diverse purposes. The present work proposes a traffic classification solution in SDN architecture using a multilayer Convolutional Neural Network. For this, statistical data collected from *Openflow* swiches are used as a way of characterizing the different categories of traffic. The proposed solution allowed the network traffic to be classified by identifying its applications with approximately 97.6% of accuracy.</div>


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
