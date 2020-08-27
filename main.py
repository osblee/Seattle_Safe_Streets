"""
Osbert Lee, Yui Suzuki, Yukito Shida
CSE 163 Section AA

This is the client to our program. The user is able to create various graphs
and maps, such as incident types that occur each month, or a map of all
incidents in seattle. Furthermore, the program is able to predict what incident
type will occur given a date and street, and also give a confidence interval
of the proportion of cases reported in spring vs fall.
"""
from make_map import Map
from make_graph import Graph
from probability import Probabilities


def run_program():
    """
    Client to run our program, asking users whether they want to use each
    feature of our program. The user may also input parameters for some
    features.
    """
    print('=-=-=-=-=-=-=-=')
    print('Welcome to Seattle Safe Streets!')
    print('Safety should never be compromised,' +
          ' so be sure to maintain awareness of your surroundings.')
    print('As a reminder, all inputted values should be in quotes.' +
          ' (i.e "Westlake Av N / John St")')
    print('=-=-=-=-=-=-=-=')
    street = input(' - Please enter a the name of a desired street' +
                   ' (if no desired street, input empty string ""): ')
    map = Map(street)
    if (not map.valid_street()):
        print('That was an incorrect street/no data found on that street name')
    else:
        print('This is a geographical, interactable map of the given street.')
        print('The points represent 911 fire calls that have')
        print('happened on that street and in the general vicinity.')
        map.g_street()
    print('=-=-=-=-=-=-=-=')
    all = input(
        ' - Would you like a map of all incident reports in Seattle (y/n): ')
    if (all == 'y'):
        print('Here is a geographical, interactable map of Seattle')
        print('and its 911 fire calls.')
        map.create_all()
    print('=-=-=-=-=-=-=-=')
    graph_vis = input(' - Would you like graphical, interactable ' +
                      'represenations of the 911 fire calls (y/n): ')
    if (graph_vis == 'y'):
        graph = Graph(map.dataset())
        graph.display_bar()
        graph.display_scatter()
    print('=-=-=-=-=-=-=-=')
    prediction = input(' - Given a street and month, would you like a' +
                       ' prediction how likely it is for a certain' +
                       ' type of 911 dial (y/n): ')
    if (prediction == 'y'):
        address = input(' - Please enter a desired street: ')
        month = input(' - Please enter a desired month (i.e. "April"): ')
        model = Probabilities(map.dataset(), address, month)
        predicted_values = model.predict()
        if (predicted_values[0] == ""):
            print('There is not enough data on this given street and' +
                  ' month to make a proper conclusion.')
        else:
            print('We are approximately ' + predicted_values[1] +
                  ' percent confident that given this street and month,' +
                  ' we predict the type of 911 dial will be:')
            print(predicted_values[0])
    print('=-=-=-=-=-=-=-=')
    confidence = input(' - Would you like to see the results of a ' +
                       'statistical confidence interval (y/n): ')
    if (confidence == 'y'):
        print('The question we asked ourselves after view the dataset is:')
        print('What is the difference in proportion of 911 fire calls in the' +
              ' Spring vs the Fall?')
        interval = Probabilities(map.dataset())
        interval_result = interval.conf_interval()
        print("We are 95 percent confident that the proportion of")
        print("cases that happen in the spring months are between")
        print(str(interval_result[0]) + ' and ' + str(interval_result[1]))
        print("higher than the proportion of cases that" +
              "happen in the fall months")
    print('=-=-=-=-=-=-=-=')
    print('Thank you for using Safe Seattle Streets. Hopefully you gained' +
          ' some new insight in your city.')


def main():
    run_program()


if __name__ == "__main__":
    main()
