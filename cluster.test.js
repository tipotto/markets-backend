const cluster = require('cluster');
const os = require('os');
const express = require('express');

// CPU のコア (スレッド) 数を調べる
const numCPUs = os.cpus().length;

if (cluster.isMaster) {
  console.log('Master');

  // Worker を生成する
  for (let i = 0; i < numCPUs; i++) {
    console.log(`Master : Cluster Fork ${i}`);
    cluster.fork();
  }

  // Worker がクラッシュしたら再生成する
  cluster.on('exit', (worker, code, signal) => {
    console.warn(
      `[${worker.id}] Worker died : [PID ${worker.process.pid}] [Signal ${signal}] [Code ${code}]`
    );
    cluster.fork();
  });
} else {
  console.log(
    `[${cluster.worker.id}] [PID ${cluster.worker.process.pid}] Worker`
  );
  // Express サーバの実装は元のまま変更なし (コンソール出力の内容だけ加工)

  express()
    .get('/', (req, res) => {
      console.log(
        `[${cluster.worker.id}] [PID ${cluster.worker.process.pid}] Request`
      );
      res.send('Hello World');
    })
    .listen(8080, () => {
      console.log(
        `[${cluster.worker.id}] [PID ${cluster.worker.process.pid}] Server Started`
      );
    });
}
