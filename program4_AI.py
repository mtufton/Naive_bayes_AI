#Meredith Tufton
#Program 4

from collections import defaultdict
import math



# tuple dictionary where index[0] is the number of spam/ham emails and
# index[1] contains the dictionary of words

spam_record = [0, defaultdict(int)]
ham_record = [0, defaultdict(int)]

def main():
    print "Name of training file for spam"
    training_file_spam = raw_input()

    print "Name of training file for ham"
    training_file_ham = raw_input()

    print "Name of testing file for spam"
    testing_file_spam = raw_input()

    print "Name of testing file for ham"
    testing_file_ham = raw_input()

    process_training_file(training_file_spam, spam_record, ham_record)
    process_training_file(training_file_ham, ham_record, spam_record)
    spam_record[1] = dict(spam_record[1])
    ham_record[1] = dict(ham_record[1])
    

##    print "Number of emails" + spam_record[0] + "vs" + ham_record[0]
##
##    print "entire vocab { "
##    vocab = 0
##
##    for key in spam_record[1]:
##        vocab += 1
##        print "' " + spam_record[1][key] "',"
##    for key in ham_record[1]:
##        vocab +=1
##        print "' " + ham_record[1][key] "',"
##    print "}"
##
##    print "entire vocab size is " + vocab
##
##    print "spam words { "
##    for key in spam_record[1]:
##        print spam_record[1][key] + ":" + key + ","
##    print "}"
##
##    print "ham words { "
##    for key in ham_record[1]:
##        print ham_record[1][key] + ":" + key + ","
##    print "}"
##
##    print "Beginning tests."
##
##    print "Testing spam emails."
##
    tot_emails = 0
    tot_correct = 0
    file2 = open(testing_file_spam, "r")
    words = file2.read().split()

    email = 0
    #list of an email contents and words
    
    words_in_subject_and_body = [] 
    for word in words:
        if word == "<SUBJECT>":
            email += 1
            tot_emails += 1
            continue
        
        #ignore end of subject, body, until end of email
        elif word != "</SUBJECT>" and word != "<BODY>" and word != "</BODY>":
            words_in_subject_and_body.append(word.lower())
        elif word == "</BODY>":
            prob_spam = log_prob_message(words_in_subject_and_body,
                                         spam_record,
                                         math.log(spam_record[0]/float(
                                             ham_record[0] +
                                             spam_record[0])))

            prob_ham = log_prob_message(words_in_subject_and_body,
                                        ham_record,
                                        math.log(ham_record[0]/float(
                                            ham_record[0] +
                                            spam_record[0])))

            if prob_spam > prob_ham:
                result = "spam"
                classification = "right"
                tot_correct += 1

            else:

                result = "ham"
                classification = "wrong"

            ## output of results of spam or ham print email + "features" assumed concatenation
            #print "TEST" + (email) + (feature_true(words_in_subject_and_body, ham_record)) + (prob_spam) + (prob_ham)  + (result) + (classification)

            print "TEST {} {}/{} features true {:.3f} {:.3f} {} {}".format(email, feature_true(words_in_subject_and_body, spam_record), len(spam_record[1]), round(prob_spam, 3), round(prob_ham, 3), result, classification)
            words_in_subject_and_body = []

        
            continue
    f = open(testing_file_ham, "r")
    words = f.read().split()

    email = 0
    words_in_subject_and_body = []
    for word in words:
        if word == "<SUBJECT>":
            email += 1
            tot_emails += 1
            continue
        elif word != "</SUBJECT>" and word != "<BODY>" and word != "</BODY>":
            words_in_subject_and_body.append(word.lower())
        elif word == "</BODY>":
            prob_spam = log_prob_message(words_in_subject_and_body,
                                         spam_record,
                                         math.log(spam_record[0]/float(
                                             ham_record[0] +
                                             spam_record[0])))

            prob_ham = log_prob_message(words_in_subject_and_body,
                                        ham_record,
                                        math.log(ham_record[0]/float(
                                            ham_record[0] +
                                            spam_record[0])))

            if prob_ham > prob_spam:
                result = "ham"
                classification = "right"
                tot_correct += 1

            else:

                result = "spam"
                classification = "wrong"

            #print "TEST" + (email) + (feature_true(words_in_subject_and_body, ham_record)) + (prob_spam) + (prob_ham)  + (result) + (classification)

            print "TEST {} {}/{} features true {:.3f} {:.3f} {} {}".format(email, feature_true(words_in_subject_and_body, spam_record), len(spam_record[1]), round(prob_spam, 3), round(prob_ham, 3), result, classification)

        
            words_in_subject_and_body = []
            continue
    print "Total {}/{} emails classified correctly".format(tot_correct, tot_emails)





def feature_true(message, record_to_test_against):
    ret = 0
    ## set creates a unique set of words to remove duplication and ignoring words
    
    for word in set(message):
        if word in record_to_test_against[1] > 0:
            ret += 1
    return ret


def train(training_set, record_to_train, opposing_record):
    words_in_set = training_set 
    record_to_train[0] += 1
    for word in words_in_set:
        record_to_train[1][word] += 1
        opposing_record[1][word] += 0

def prob_word(word, record_to_test_against):
    return (record_to_test_against[1][word.lower()]+1)/float(record_to_test_against[0]+2)
    
def prob_not_word(word, record_to_test_against):
    tot_emails = record_to_test_against[0]
    orig_num = record_to_test_against[1][word.lower()]
    new_num = tot_emails - orig_num + 1
    return new_num/float(record_to_test_against[0]+2)

# log_prior_prob will be math.log(num_spam_emails/total_num_emails)
def log_prob_message(message, record_to_test_against, log_prior_prob):
    #words = []
    #for word in message:
    #    if word in record_to_test_against[1]:
    #        words.append(word)
    #liklihood = [prob_word(word, record_to_test_against) for word in words]
    liklihood = []
    for word in record_to_test_against[1].keys():
        if word in message:
           liklihood.append(prob_word(word, record_to_test_against))
        else:
            liklihood.append(prob_not_word(word, record_to_test_against))
    
    return sum([math.log(wl) for wl in liklihood]) + log_prior_prob
    

def process_training_file(fname, record_to_train, opposing_record):
# collect words from subject and body of each email
    #for each email:
    file = open(fname, "r")
    words = file.read().split()
    words_in_email = set()
    for word in words:
        if word == "<SUBJECT>":
            continue
        elif word != "</SUBJECT>" and word != "<BODY>" and word != "</BODY>":
            words_in_email.add(word.lower())
        elif word == "</BODY>":
            train(words_in_email, record_to_train, opposing_record)
            words_in_email = set()
            continue  


main()
