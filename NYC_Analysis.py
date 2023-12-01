import preprocess_utils as pu
import data_utils as du

def main():
    datasets = du.import_data()
    datasets = pu.preprocess_datasets(datasets)

    # 'LAW_CAT_CD' is the target variable to predict
    target_variable = 'Crime Category'

    # Selecting features and target variable
    features = datasets['Drug_Crime'].drop(columns=[target_variable, 'Lat_Lon', 'Phone', 'Address'])
    target = datasets['Drug_Crime'][target_variable]

    # Handling missing values
    numeric_features = features.select_dtypes(include=['float64']).columns
    categorical_features = features.select_dtypes(include=['object']).columns

    imputer_numeric = SimpleImputer(strategy='mean')
    features[numeric_features] = imputer_numeric.fit_transform(features[numeric_features])

    imputer_categorical = SimpleImputer(strategy='most_frequent')
    features[categorical_features] = imputer_categorical.fit_transform(features[categorical_features])

    # Handling categorical variables
    features = pd.get_dummies(features)

    # Splitting the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Initializing and training a Random Forest Classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Making predictions on the test set
    y_pred = clf.predict(X_test)

    # Evaluating the model
    accuracy = accuracy_score(y_test, y_pred)
    classification_report_result = classification_report(y_test, y_pred)

    # Printing results
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", classification_report_result)

if __name__ == '__main__':
    main()