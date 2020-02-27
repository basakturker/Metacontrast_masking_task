from psychopy import core, visual, gui, data, event, monitors
import random
import pandas as pd
import os
import os.path as op
import numpy
exp_name = 'metacontrast_staircase'
exp_info = {'Participant': ''}
dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
if dlg.OK is False:
    core.quit()
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name


home_dir = '/home/fraimondo/Bertrand/Metacontrast_task'
script_dir = op.join(home_dir, 'Scripts')
images_dir = op.join(home_dir, 'Images')
data_dir = op.join(home_dir, 'Data')
participant_dir = op.join(data_dir, '{}'.format(exp_info['Participant']))
if not op.exists(participant_dir):
    os.mkdir(participant_dir)

filename = op.join(participant_dir, '{}_{}_{}'.format(
    exp_info['Participant'],
    exp_name,
    exp_info['date']))

win = visual.Window([1920, 1080],
                    monitor='Dell precision',
                    fullscr=True,
                    screen=1,
                    units='norm',
                    color='gainsboro') #gainsboro

fixation = visual.SimpleImageStim(win=win,
                                  image=op.join(images_dir, 'cross_grey.tif'))
dotUR = visual.ImageStim(win=win,
                         image=op.join(images_dir, 'dot_grey.tif'),
                         size=0.02)
dotUL = visual.ImageStim(win=win,
                         image=op.join(images_dir, 'dot_grey.tif'),
                         size=0.02)
dotDR = visual.ImageStim(win=win,
                         image=op.join(images_dir, 'dot_grey.tif'),
                         size=0.02)
dotDL = visual.ImageStim(win=win,
                         image=op.join(images_dir, 'dot_grey.tif'),
                         size=0.02)

t7 = visual.TextStim(win=win, text='7',units='norm', height=0.15, color='black')

t2 = visual.TextStim(win=win, text='2',units='norm', height=0.15, color='black')

t8 = visual.TextStim(win=win, text='8',units='norm', height=0.15, color='black')

t3 = visual.TextStim(win=win, text='3',units='norm', height=0.15, color='black')

mask_image = visual.SimpleImageStim(win=win,
                                    image=op.join(images_dir, 'mask3_grey.tif'))

scale_rating1 = visual.RatingScale(win=win,
                                   lineColor='black',
                                   # low=0, high=1,
                                   choices=['non vu', " ", 'vu'],
                                   markerStart=1,
                                   textColor='black',
                                   pos=(0, 0),
                                   noMouse=True,
                                   scale=None,
                                   marker='triangle',
                                   markerColor='DarkRed',
                                   showAccept=False,
                                   acceptKeys=['space', 'num_enter'])
scale_rating2 = visual.RatingScale(win=win,
                                   lineColor='black',
                                   # low=0, high=1,
                                   choices=['vu', " ", 'non vu'],
                                   markerStart=1,
                                   textColor='black',
                                   pos=(0, 0),
                                   noMouse=True,
                                   scale=None,
                                   marker='triangle',
                                   markerColor='DarkRed',
                                   showAccept=False,
                                   acceptKeys=['space', 'num_enter'])

#
# fixation.draw()
# win.flip()
core.wait(1)
trial=0
SOA_trials=random.sample(range(10,380),100)
SOA_trials_SOA=[1,2,4,5]*25
random.shuffle(SOA_trials_SOA)
staircase = data.StairHandler(0.7, 0.2, stepSizes=[0.02], nUp=1, nDown=1, stepType='lin',
    nTrials=400, minVal=-1, maxVal=1)
resp=[]
cont=[]
ObjR=[]
SOA=[]
for contrast in staircase:
    a=random.randint(1,4)
    if a==1:
        t=t2
    if a==2:
        t=t3
    if a==3:
        t=t7
    if a==4:
        t=t8
    t.contrast = contrast
    po=[(-0.14,0.0),(0.14,0.0)]
    p=random.choice(po)
    t.setPos(p)
    mask_image.setPos(p)
    dotUR.pos = (0.5, 0.5)
    dotUL.pos = (-0.5, 0.5)
    dotDR.pos = (0.5, -0.5)
    dotDL.pos = (-0.5, -0.5)
    fixation.setAutoDraw(True)
    for frameN in range(20):
        dotUR.pos *= 0.87
        dotUL.pos *= 0.87
        dotDR.pos *= 0.87
        dotDL.pos *= 0.87
        dotUR.draw()
        dotUL.draw()
        dotDR.draw()
        dotDL.draw()
        win.flip()

    for frameN in range(1):
        t.draw()
        win.flip()
    if trial not in SOA_trials:
        for frameN in range(3):
            win.flip()
        SOA.append(3)
    else:
        for frameN in range(SOA_trials_SOA[0]):
            win.flip()
        SOA.append(SOA_trials_SOA[0])
        SOA_trials_SOA.remove(SOA_trials_SOA[0])

    for frameN in range(15):
        mask_image.setAutoDraw(True)
        win.flip()
    mask_image.setAutoDraw(False)
    fixation.setAutoDraw(False)
    win.flip()
    for frameN in range(30):
        win.flip()
    obj_order = visual.TextStim(
        win=win,
        text='Comparaison au nombre 5',
        color='black')
    obj_order.draw()
    win.flip()
    obj_rating = event.waitKeys(keyList=['left', 'right'])
    if (t==t2 or t==t3) and obj_rating==['left']:
        OR=1
    if (t==t2 or t==t3) and obj_rating==['right']:
        OR=0
    if (t==t7 or t==t8) and obj_rating==['left']:
        OR=0
    if (t==t7 or t==t8) and obj_rating==['right']:
        OR=1
    ObjR.append(OR)
    scale_order=random.randint(1,2)
    if scale_order==1:
        scaleR=scale_rating1
    else:
        scaleR=scale_rating2
    subj = visual.TextStim(
        win=win,
        text='Avez-vous vu la cible?',
        pos=(0.0,0.3),
        color='black')
    while scaleR.noResponse:
        scaleR.draw()
        subj.draw()
        win.flip()

    SR = scaleR.getRating()

    while SR == " ":
        scaleR.reset()
        while scaleR.noResponse:
            scaleR.draw()
            subj.draw()
            win.flip()
        SR = scaleR.getRating()

    if SR == "non vu":
        response = 0
        print("non")
    else:
        response = 1
        print("yes")
    resp.append(response)
    cont.append(contrast)
    if trial not in SOA_trials:
        staircase.addResponse(response)
    scaleR.reset()
    if trial==199:
        textPause = visual.TextStim(
            win=win,
            text="A partir de maintenant repondez avec votre autre main. \n"
            "Appuyez sur l'espace ou sur l'enter pour continuer",
            color='black')
        textPause.draw()
        win.flip()
        event.waitKeys(keyList=['space', 'num_enter'])
        for frameN in range(40):
            win.flip()
    trial=trial+1
    core.wait(0.2)
    win.flip()
fixation.setAutoDraw(False)
print('reversals:')
print(staircase.reversalIntensities)
print('mean of final 8 reversals = %.3f' % numpy.average(staircase.reversalIntensities[-8:]))
stairC_df = pd.DataFrame({
    'SOA': SOA,
    'contrast': cont,
    'subj_response': resp,
    'obj_response': ObjR})

stairC_df.to_excel(filename+'.xlsx')
stairC_df.to_csv(filename+'.csv',sep=';')
win.close()
