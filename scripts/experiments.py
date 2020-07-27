import os
import sys
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(FILE_PATH, '..'))
sys.path.append(ROOT_PATH)
sys.path.insert(0, os.path.join(ROOT_PATH, 'build/Release' if os.name == 'nt' else 'build'))
from tensorpack.utils.stats import StatCounter
from tensorpack.utils.utils import get_tqdm
from multiprocessing import *
from datetime import datetime
from envs import make_env
from agents import make_agent

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

types = ['CDQN', 'RANDOM', 'RANDOM']


def eval_episode(env, agent):
    env.reset()
    env.prepare()
    done = False
    r = 0
    while not done:
        print("env role ID" + str(env.get_role_ID())+ " agent role id " + str(agent.role_id))
        if env.get_role_ID() != agent.role_id:
            r, done = env.step_auto()
        else:
            r, done = env.step(agent.intention(env))
    if agent.role_id == 2:
        r = -r
    assert r != 0
    return int(r > 0)


def eval_proc(file_name):
    print(file_name)
    f = open(os.path.join('./log') + file_name, 'w+')
    for te in types:
        for ta in types:
            for role_id in [2, 3, 1]:
                agent = make_agent(ta, role_id)
                for i in range(1):
                    env = make_env(te)
                    st = StatCounter()
                    with get_tqdm(total=100) as pbar:
                        for j in range(100):
                            winning_rate = eval_episode(env, agent)
                            st.feed(winning_rate)
                            pbar.update()
                    f.write('%s with role id %d against %s, winning rate: %f\n' % (ta, role_id, te, st.average))
    f.close()

def onlytest():
    # env = make_env('RHCP')
    #env = make_env('RANDOM')
    #env = make_env('MCT')
    # env = make_env('CDQN')
    
    env = make_env('CDQN')
    agent = make_agent('RANDOM', 1)
    eval_episode(env, agent)

if __name__ == '__main__':
    onlytest();
    # eval_proc('res_.txt')
    # procs = []
    # for i in range(cpu_count() // 2):
    #     procs.append(Process(target=eval_proc, args=('res%d.txt' % i,)))
    # for p in procs:
    #     p.start()
    # for p in procs:
    #     p.join()


