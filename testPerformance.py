from metrics import precision
import numpy as np


# adult probation
print('-------------------------------------- Adult Probation --------------------------------------')

actual_adult_probation_adam = ['2959732','150543','146790','146553','111105','110896','110585','110425','108785','101183']
print('actual_adult_probation_adam: ', actual_adult_probation_adam)

predictd_adult = [[110117, 0.45648130703581674], [110585, 0.4285737737881382], [146790, 0.40441472797427647], [2959732, 0.34090307630334943], [107693, 0.3342951043682529], [146553, 0.32676667267588216], [108785, 0.3256834050257937], [109093, 0.32430868339245533], [109775, 0.3084585056242143], [111105, 0.2891431612767075], [150543, 0.2715544427348346], [110425, 0.26700141561834106], [110896, 0.2632105162435864], [107439, 0.2604221962354819], [111977, 0.2599154005857053], [101183, 0.25571265883711564], [111198, 0.25346496019722], [107191, 0.2297795760028584], [109258, 0.2238365716979934], [109842, 0.176073844381976]]
predictd_adult_without_score = [str(id) for [id, _] in predictd_adult]
print('predictd_adult_without_score: ', predictd_adult_without_score)

# use for test average precision
# score_ap = precision.apk(actual = actual_adult_probation_adam, predicted=predictd_adult_without_score, k=2)
# print('score_ap: ', score_ap)

# score_map = precision.mapk(actual = actual_adult_probation_adam, predicted=predictd_adult_without_score, k=2)
# print('Mean average precision: ',score_map)

# compute average precision on adult probation
score_ap_adult_probation = []
for i in range(1,21):
    score_ap = precision.apk(actual = actual_adult_probation_adam, predicted=predictd_adult_without_score, k=i)
    score_ap_adult_probation.append(score_ap)
    print('Average precision for top %d is %f' %(i, score_ap))

# mail fraud
print('-------------------------------------- Mail Fraud --------------------------------------')
actual_mail_fraud_adam = ['1740','145799','145652','118390','118298','118143','112222','111964','111945','110375','108900','105186','104727',
                          '104481','104518']
print('actual_mail_fraud_adam: ', actual_mail_fraud_adam)
predictd_mail_fraud = [[112222, 0.5137677282981165], [108900, 0.4248894330337993], [111945, 0.40739488118809464], [111964, 0.40307292674491313], [118298, 0.3755608980692612], [2680440, 0.3490712791165256], [2679833, 0.34414200359639824], [105186, 0.3278959670858562], [145652, 0.28449791187818335], [145799, 0.26150023796417715], [1740, 0.2563420769743946], [118390, 0.251663846218966], [110375, 0.24898893161587587], [104727, 0.2431552348214463], [118143, 0.2364249929461651], [96830, 0.22676586696437007], [104481, 0.22275152951976168], [104518, 0.20973750472517277], [105129, 0.20880888358431], [107516, 0.20356786565421148]]
predictd_mail_fraud_without_score = [str(id) for [id, _] in predictd_mail_fraud]
print('predictd_mail_fraud_without_score: ', predictd_mail_fraud_without_score)
# compute average precision on mail fraud
score_ap_mail_fraud = []
for i in range(1,21):
    score_ap = precision.apk(actual = actual_mail_fraud_adam, predicted=predictd_mail_fraud_without_score, k=i)
    score_ap_mail_fraud.append(score_ap)
    print('Average precision for top %d is %f' %(i, score_ap))

print('-------------------------------------- Mean Average Precision --------------------------------------')
score_ap_adult_probation = np.asarray(score_ap_adult_probation)
score_ap_mail_fraud = np.asarray(score_ap_mail_fraud)
print('score_ap_adult_probation: ', score_ap_adult_probation)
print('score_ap_mail_fraud: ', score_ap_mail_fraud)

score_map = (score_ap_adult_probation + score_ap_mail_fraud)/2
print('total: ', score_map)










