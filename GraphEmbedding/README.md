基于 word2vec 的一系列 embedding 方法主要是基于序列进行 embedding，在当前商品、行为、用户等实体之间的关系越来越复杂化、网络化的趋势下，原有 sequence embedding 方法的表达能力受限，因此 Graph Embedding 方法的研究和应用成为了当前的趋势。

1. [DeepWalk] DeepWalk- Online Learning of Social Representations (SBU 2014)

以随机游走的方式从网络中生成序列，进而转换成传统 word2vec 的方法生成 Embedding。这篇论文可以视为 Graph Embedding 的 baseline 方法，用极小的代价完成从 word2vec 到 graph embedding 的转换和工程尝试。

2. [LINE] LINE - Large-scale Information Network Embedding (MSRA 2015)

相比 DeepWalk 纯粹随机游走的序列生成方式，LINE 可以应用于有向图、无向图以及边有权重的网络，并通过将一阶、二阶的邻近关系引入目标函数，能够使最终学出的 node embedding 的分布更为均衡平滑，避免 DeepWalk 容易使 node embedding 聚集的情况发生。

3. [Node2vec] Node2vec - Scalable Feature Learning for Networks (Stanford 2016)

node2vec 这篇文章还是对 DeepWalk 随机游走方式的改进。为了使最终的 embedding 结果能够表达网络局部周边结构和整体结构，其游走方式结合了深度优先搜索和广度优先搜索。

4. [SDNE] Structural Deep Network Embedding (THU 2016)

相比于 node2vec 对游走方式的改进，SDNE 模型主要从目标函数的设计上解决 embedding 网络的局部结构和全局结构的问题。而相比 LINE 分开学习局部结构和全局结构的做法，SDNE 一次性的进行了整体的优化，更有利于获取整体最优的 embedding。

5. [Alibaba Embedding] Billion-scale Commodity Embedding for E-commerce Recommendation in Alibaba (Alibaba 2018)

阿里巴巴在 KDD 2018 上发表的这篇论文是对 Graph Embedding 非常成功的应用。从中可以非常明显的看出从一个原型模型出发，在实践中逐渐改造，最终实现其工程目标的过程。这个原型模型就是上面提到的 DeepWalk，阿里通过引入 side information 解决 embedding 问题非常棘手的冷启动问题，并针对不同 side information 进行了进一步的改造形成了最终的解决方案 EGES（Enhanced Graph Embedding with Side Information）。
